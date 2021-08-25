/*
 *
 *  This file is part of the scientific research and development work conducted
 *  at the Communication Networks Institute (CNI), TU Dortmund University.
 *
 *  Copyright (C) 2021 Communication Networks Institute (CNI)
 *  Technische Universität Dortmund
 *
 *  Contact: kn.etit@tu-dortmund.de
 *  Authors: Fabian Eckermann
 *           fabian.eckermann@tu-dortmund.de
 *
 *  This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU Affero General Public License for more details.
 *
 * A copy of the GNU Affero General Public License can be found in
 * the LICENSE file in the top-level directory of this distribution
 * and at http://www.gnu.org/licenses/.
 *
 * For more information on this software, see the institute's project website at:
 * http://www.cni.tu-dortmund.de
 *
 */

/*
 * Copyright 2013-2020 Software Radio Systems Limited
 *
 * This file is part of srsLTE.
 *
 * srsLTE is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of
 * the License, or (at your option) any later version.
 *
 * srsLTE is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * A copy of the GNU Affero General Public License can be found in
 * the LICENSE file in the top-level directory of this distribution
 * and at http://www.gnu.org/licenses/.
 *
 */

#include "srslte/srslte.h"
#include <complex.h>
#include <math.h>
#include <string.h>

#include "srslte/phy/ue/ue_sl.h"

#define CURRENT_FFTSIZE srslte_symbol_sz(q->cell.nof_prb)
#define CURRENT_SFLEN SRSLTE_SF_LEN(CURRENT_FFTSIZE)

#define CURRENT_SLOTLEN_RE SRSLTE_SLOT_LEN_RE(q->cell.nof_prb, q->cell.cp)
#define CURRENT_SFLEN_RE SRSLTE_NOF_RE(q->cell)

#define MAX_SFLEN SRSLTE_SF_LEN(srslte_symbol_sz(max_prb))


int srslte_ue_sl_init(srslte_ue_sl_t* q,
                      srslte_cell_sl_t cell,
                      srslte_sl_comm_resource_pool_t sl_comm_resource_pool,
                      uint32_t nof_rx_antennas)
{
  int ret = SRSLTE_ERROR_INVALID_INPUTS;

  if (q != NULL) {
    ret = SRSLTE_ERROR;

    bzero(q, sizeof(srslte_ue_sl_t));

    q->cell = cell;
    q->sl_comm_resource_pool = sl_comm_resource_pool;
    q->nof_rx_antennas = nof_rx_antennas;
    q->sf_len = SRSLTE_SF_LEN_PRB(q->cell.nof_prb);  // 1ms worth of samples

    q->sf_symbols_tx = srslte_vec_cf_malloc(q->sf_len);
    if (!q->sf_symbols_tx) {
      perror("malloc");
      goto clean_exit;
    }

    q->signal_buffer_tx = srslte_vec_cf_malloc(q->sf_len);
    if (!q->signal_buffer_tx) {
      perror("malloc");
      goto clean_exit;
    }
    srslte_vec_cf_zero(q->signal_buffer_tx, q->sf_len);

    /** Init TX IFFT **/
    srslte_ofdm_cfg_t ofdm_cfg_tx = {};
    ofdm_cfg_tx.nof_prb           = q->cell.nof_prb;
    ofdm_cfg_tx.in_buffer         = q->sf_symbols_tx;
    ofdm_cfg_tx.out_buffer        = q->signal_buffer_tx;
    ofdm_cfg_tx.cp                = SRSLTE_CP_NORM;
    ofdm_cfg_tx.freq_shift_f      = 0.5f;
    ofdm_cfg_tx.normalize         = true;
    ofdm_cfg_tx.sf_type           = SRSLTE_SF_NORM;
    if (srslte_ofdm_tx_init_cfg(&q->ifft, &ofdm_cfg_tx)) {
      ERROR("Error initiating IFFT\n");
      goto clean_exit;
    }

    /** Init RX FFT **/
    for (int i = 0; i < q->nof_rx_antennas; i++) {
      q->signal_buffer_rx[i] = srslte_vec_cf_malloc(q->sf_len);
      if (!q->signal_buffer_rx[i]) {
        perror("malloc");
        exit(-1);
      }
      q->sf_symbols_rx[i] = srslte_vec_cf_malloc(q->sf_len);
      if (!q->sf_symbols_rx[i]) {
        perror("malloc");
        goto clean_exit;
      }
      srslte_vec_cf_zero(q->signal_buffer_rx[i], q->sf_len);
      srslte_vec_cf_zero(q->sf_symbols_rx[i], q->sf_len);
    }

    q->sf_n_re = SRSLTE_CP_NSYMB(SRSLTE_CP_NORM) * SRSLTE_NRE * 2 * q->cell.nof_prb;
    q->equalized_sf_buffer = srslte_vec_cf_malloc(sizeof(cf_t) * q->sf_n_re);

    srslte_ofdm_cfg_t ofdm_cfg_rx = {};
    ofdm_cfg_rx.nof_prb           = q->cell.nof_prb;
    ofdm_cfg_rx.cp                = SRSLTE_CP_NORM;
    ofdm_cfg_rx.rx_window_offset  = 0.0f;
    ofdm_cfg_rx.freq_shift_f      = -0.5f;
    ofdm_cfg_rx.normalize         = true;
    ofdm_cfg_rx.sf_type           = SRSLTE_SF_NORM;

    for (int i = 0; i < q->nof_rx_antennas; i++) {
      ofdm_cfg_rx.in_buffer  = q->signal_buffer_rx[0];
      ofdm_cfg_rx.out_buffer = q->sf_symbols_rx[0];

      if (srslte_ofdm_rx_init_cfg(&q->fft[i], &ofdm_cfg_rx)) {
        ERROR("Error initiating FFT\n");
        goto clean_exit;
      }
    }

    // init tx
    if (srslte_pscch_init(&q->pscch_tx, SRSLTE_MAX_PRB)) {
      ERROR("Error creating PSCCH object\n");
      goto clean_exit;
    }

    if (srslte_sci_init(&q->sci_tx, q->cell, q->sl_comm_resource_pool)) {
      ERROR("Error creating SCI TX object\n");
      goto clean_exit;
    }

    if (srslte_pssch_init(&q->pssch_tx, q->cell, q->sl_comm_resource_pool)) {
      ERROR("Error creating PSSCH object\n");
      goto clean_exit;
    }

    if (srslte_chest_sl_init(&q->pscch_chest_tx, SRSLTE_SIDELINK_PSCCH, q->cell, q->sl_comm_resource_pool)) {
      ERROR("Error creating PSCCH chest object\n");
      goto clean_exit;
    }

    if (srslte_chest_sl_init(&q->pssch_chest_tx, SRSLTE_SIDELINK_PSSCH, q->cell, q->sl_comm_resource_pool)) {
      ERROR("Error creating PSSCH chest object\n");
      goto clean_exit;
    }

    // init rx
    for (uint32_t subch_idx = 0; subch_idx < q->sl_comm_resource_pool.num_sub_channel; subch_idx++)
    {
      if (srslte_pscch_init(&q->pscch_rx[subch_idx], SRSLTE_MAX_PRB)) {
        ERROR("Error creating PSCCH object\n");
        goto clean_exit;
      }

      if (srslte_sci_init(&q->sci_rx[subch_idx], q->cell, q->sl_comm_resource_pool)) {
        ERROR("Error creating SCI RX object for sub channel %d\n", subch_idx);
        goto clean_exit;
      }

      if (srslte_pssch_init(&q->pssch_rx[subch_idx], q->cell, q->sl_comm_resource_pool)) {
        ERROR("Error creating PSSCH object\n");
        goto clean_exit;
      }

      if (srslte_chest_sl_init(&q->pscch_chest_rx[subch_idx], SRSLTE_SIDELINK_PSCCH, q->cell, q->sl_comm_resource_pool)) {
        ERROR("Error creating PSCCH chest object\n");
        goto clean_exit;
      }

      if (srslte_chest_sl_init(&q->pssch_chest_rx[subch_idx], SRSLTE_SIDELINK_PSSCH, q->cell, q->sl_comm_resource_pool)) {
        ERROR("Error creating PSSCH chest object\n");
        goto clean_exit;
      }
    }

    if (srslte_ue_sl_set_cell(q, q->cell)) {
      ERROR("Error setting cell\n");
      goto clean_exit;
    }

    ret = SRSLTE_SUCCESS;
  } else {
    ERROR("Invalid parameters\n");
  }

clean_exit:
  if (ret == SRSLTE_ERROR) {
    srslte_ue_sl_free(q);
  }
  return ret;
}

void srslte_ue_sl_free(srslte_ue_sl_t* q)
{
  if (q) {
    // free tx
    srslte_ofdm_tx_free(&q->ifft);
    srslte_pscch_free(&q->pscch_tx);
    srslte_pssch_free(&q->pssch_tx);
    srslte_sci_free(&q->sci_tx);
    srslte_chest_sl_free(&q->pscch_chest_tx);
    srslte_chest_sl_free(&q->pssch_chest_tx);

    // free rx
    for (int port = 0; port < SRSLTE_MAX_PORTS; port++) {
      srslte_ofdm_rx_free(&q->fft[port]);
      if (q->sf_symbols_rx[port]) {
        free(q->sf_symbols_rx[port]);
      }
    }
    for (uint32_t subch_idx = 0; subch_idx < SRSLTE_MAX_NUM_SUB_CHANNEL; subch_idx++)
    {
      srslte_pscch_free(&q->pscch_rx[subch_idx]);
      srslte_pssch_free(&q->pssch_rx[subch_idx]);
      srslte_sci_free(&q->sci_rx[subch_idx]);
      srslte_chest_sl_free(&q->pscch_chest_rx[subch_idx]);
      srslte_chest_sl_free(&q->pssch_chest_rx[subch_idx]);
    }

    if (q->sf_symbols_tx) {
      free(q->sf_symbols_tx);
    }

    bzero(q, sizeof(srslte_ue_sl_t));
  }
}

int srslte_ue_sl_set_cell(srslte_ue_sl_t* q, srslte_cell_sl_t cell)
{
  q->cell = cell;

  if (srslte_ofdm_tx_set_prb(&q->ifft, q->cell.cp, q->cell.nof_prb)) {
    ERROR("Error resizing IFFT\n");
    return SRSLTE_ERROR;
  }

  if (srslte_pscch_set_cell(&q->pscch_tx, q->cell)) {
    ERROR("Error resizing PSCCH object\n");
    return SRSLTE_ERROR;
  }

  for (int port = 0; port < q->nof_rx_antennas; port++) {
    if (srslte_ofdm_rx_set_prb(&q->fft[port], q->cell.cp, q->cell.nof_prb)) {
      ERROR("Error resizing FFT\n");
      return SRSLTE_ERROR;
    }
  }

  for (uint32_t subch_idx = 0; subch_idx < q->sl_comm_resource_pool.num_sub_channel; subch_idx++) {
    if (srslte_pscch_set_cell(&q->pscch_rx[subch_idx], q->cell)) {
      ERROR("Error resizing PSCCH object\n");
      return SRSLTE_ERROR;
    }
  }

  return SRSLTE_SUCCESS;
}

int srslte_ue_sl_set_sl_comm_resource_pool(srslte_ue_sl_t* q, srslte_sl_comm_resource_pool_t sl_comm)
{
  q->sl_comm_resource_pool = sl_comm;
  return SRSLTE_SUCCESS;
}

/**
 * Calculate N_x_id from crc (3GPP TS 36.211 sec. 9.3.1).
 *
 * @param crc the crc value array
 * @param crc_len length of crc value array
 * @return N_x_id
 */
uint32_t srslte_n_x_id_from_crc(uint8_t *crc, uint32_t crc_len)
{
  uint32_t N_x_id = 0;
  for (int j = 0; j < crc_len; j++) {
    N_x_id += crc[j] * exp2(crc_len - 1 - j);
  }
  return N_x_id;
}

/**
 * Calculate sci resource reservation value from resource reservation interval (3GPP TS 36.213 sec. 14.2.1).
 *
 * @param resource_reserv_intvl resource reservation interval in ms ([20, 50, 100, 200, 300, ... 1000])
 * @return resource_reserv
 */
uint32_t srslte_intvl_to_reserv(uint32_t resource_reserv_intvl)
{
  switch (resource_reserv_intvl) {
    case 20:
      return 12;
    case 50:
      return 11;
    default:
      if (resource_reserv_intvl % 100 == 0 && resource_reserv_intvl <= 1000) {
        return resource_reserv_intvl / 100;
      } else {
        ERROR("Error invalid resource reservation interval. Valid values are [20, 50, 100, 200, 300, ... 1000]\n");
        exit(-1);
      }
  }
}

/**
 * Calculate resource reservation interval in ms from sci resource reservation value (3GPP TS 36.213 sec. 14.2.1).
 *
 * @param resource_reserv sci resource reservation value
 * @return resource reservation interval in ms ([20, 50, 100, 200, 300, ... 1000])
 */
uint32_t srslte_intvl_from_reserv(uint32_t resource_reserv)
{
  switch (resource_reserv) {
    case 12:
      return 20;
    case 11:
      return 50;
    default:
      return resource_reserv * 100;
  }
}

/**
 * Set sci parameters.
 *
 * Reference:  3GPP TS 36.212 version 15.6.0 Release 15 Section 5.4.3
 *
 * @param sci object
 * @param priority priority
 * @param resource_reserv_intvl resource reservation interval in ms ([20, 50, 100, 200, 300, ... 1000])
 * @param time_gap time_gap
 * @param retransmission retransmission
 * @param transmission_format transmission format
 * @param mcs_idx mcs index
 */
void srslte_set_sci(srslte_sci_t* sci,
                    uint32_t priority,
                    uint32_t resource_reserv_itvl,
                    uint32_t time_gap,
                    bool     retransmission,
                    uint32_t transmission_format,
                    uint32_t mcs_idx)
{
  sci->priority            = priority;
  sci->resource_reserv     = srslte_intvl_to_reserv(resource_reserv_itvl);
  sci->time_gap            = time_gap;
  sci->retransmission      = retransmission;
  sci->transmission_format = transmission_format;
  sci->mcs_idx             = mcs_idx;
}

void srslte_set_sci_riv(srslte_ue_sl_t* q, uint32_t sub_channel_start_idx, uint32_t l_sub_channel)
{
  q->sci_tx.riv = srslte_ra_sl_type0_to_riv(
      q->sl_comm_resource_pool.num_sub_channel, sub_channel_start_idx, l_sub_channel);
}

/* Generate PSCCH signal
 */
static int pscch_encode(srslte_ue_sl_t* q, uint32_t sub_channel_start_idx)
{

  int ret = SRSLTE_ERROR_INVALID_INPUTS;

  if (q != NULL) {

    srslte_vec_cf_zero(q->sf_symbols_tx, SRSLTE_NOF_RE(q->cell));

    uint32_t pscch_prb_start_idx = sub_channel_start_idx * q->sl_comm_resource_pool.size_sub_channel;

    uint8_t sci_tx[SRSLTE_SCI_MAX_LEN] = {};
    if (q->sci_tx.format == SRSLTE_SCI_FORMAT0) {
      if (srslte_sci_format0_pack(&q->sci_tx, sci_tx) != SRSLTE_SUCCESS) {
        printf("Error packing SCI Format 0\n");
        return SRSLTE_ERROR;
      }
    } else if (q->sci_tx.format == SRSLTE_SCI_FORMAT1) {
      if (srslte_sci_format1_pack(&q->sci_tx, sci_tx) != SRSLTE_SUCCESS) {
        printf("Error packing SCI Format 1\n");
        return SRSLTE_ERROR;
      }
    }

    if (srslte_pscch_encode(&q->pscch_tx, sci_tx, q->sf_symbols_tx, pscch_prb_start_idx)) {
      ERROR("Error encoding PSCCH\n");
      return SRSLTE_ERROR;
    }

    srslte_chest_sl_cfg_t pscch_chest_sl_cfg;
    pscch_chest_sl_cfg.prb_start_idx = pscch_prb_start_idx;
    pscch_chest_sl_cfg.cyclic_shift = 0;
    srslte_chest_sl_set_cfg(&q->pscch_chest_tx, pscch_chest_sl_cfg);
    srslte_chest_sl_put_dmrs(&q->pscch_chest_tx, q->sf_symbols_tx);

    ret = SRSLTE_SUCCESS;
  }

  return ret;
}

/* Generate PSSCH signal
 */
static int pssch_encode(srslte_ue_sl_t* q,
                        srslte_sl_sf_cfg_t* sf,
                        srslte_pssch_data_t* data)
{
  int ret = SRSLTE_ERROR_INVALID_INPUTS;

  if (q != NULL) {
    ret = SRSLTE_ERROR;

    uint32_t pscch_prb_start_idx = data->sub_channel_start_idx * q->sl_comm_resource_pool.size_sub_channel;
    uint32_t pssch_prb_start_idx_tx = pscch_prb_start_idx + q->pscch_tx.pscch_nof_prb;

    uint8_t *sci_crc = srslte_vec_u8_malloc(SRSLTE_SCI_CRC_LEN);
    memcpy(sci_crc, &q->pscch_tx.c[q->pscch_tx.sci_len], sizeof(uint8_t) * SRSLTE_SCI_CRC_LEN);
    uint32_t N_x_id = srslte_n_x_id_from_crc(sci_crc, SRSLTE_SCI_CRC_LEN);
    free(sci_crc);

    uint32_t rv_idx = 0;
    if (q->sci_tx.retransmission == true) {
      rv_idx = 1;
    }
    uint32_t nof_prb_pssch = data->l_sub_channel * q->sl_comm_resource_pool.size_sub_channel - q->pscch_tx.pscch_nof_prb;
    nof_prb_pssch = srslte_dft_precoding_get_valid_prb(nof_prb_pssch);

    srslte_pssch_cfg_t pssch_cfg = {pssch_prb_start_idx_tx, nof_prb_pssch, N_x_id, q->sci_tx.mcs_idx, rv_idx, sf->tti % 10};
    if (srslte_pssch_set_cfg(&q->pssch_tx, pssch_cfg)) {
      ERROR("Error configuring PSSCH\n");
      return SRSLTE_ERROR;
    }

    INFO("PSSCH TX: prb_start_idx: %d, nof_prb: %d, N_x_id: %d, mcs_idx: %d, rv_idx: %d, sf_idx: %d\n",
         q->pssch_tx.pssch_cfg.prb_start_idx,
         q->pssch_tx.pssch_cfg.nof_prb,
         q->pssch_tx.pssch_cfg.N_x_id,
         q->pssch_tx.pssch_cfg.mcs_idx,
         q->pssch_tx.pssch_cfg.rv_idx,
         q->pssch_tx.pssch_cfg.sf_idx);

    if (srslte_pssch_encode(&q->pssch_tx, data->ptr, q->pssch_tx.sl_sch_tb_len, q->sf_symbols_tx)) {
      ERROR("Error encoding PSSCH\n");
      return SRSLTE_ERROR;
    }

    srslte_chest_sl_cfg_t pssch_chest_sl_cfg;
    pssch_chest_sl_cfg.N_x_id        = N_x_id;
    pssch_chest_sl_cfg.sf_idx        = sf->tti % 10;
    pssch_chest_sl_cfg.prb_start_idx = pssch_prb_start_idx_tx;
    pssch_chest_sl_cfg.nof_prb       = nof_prb_pssch;
    srslte_chest_sl_set_cfg(&q->pssch_chest_tx, pssch_chest_sl_cfg);
    srslte_chest_sl_put_dmrs(&q->pssch_chest_tx, q->sf_symbols_tx);

    ret = SRSLTE_SUCCESS;
  }

  return ret;
}

int srslte_ue_sl_encode(srslte_ue_sl_t* q,
                        srslte_sl_sf_cfg_t* sf,
                        srslte_pssch_data_t* data)
{

  srslte_set_sci_riv(q, data->sub_channel_start_idx, data->l_sub_channel);

  if (pscch_encode(q, data->sub_channel_start_idx)) {
    return SRSLTE_ERROR;
  }
  if (pssch_encode(q, sf, data)) {
    return SRSLTE_ERROR;
  }

  srslte_ofdm_tx_sf(&q->ifft);

  srslte_vec_cf_zero(q->sf_symbols_tx, q->sf_len);

  return SRSLTE_SUCCESS;
}

int srslte_ue_sl_decode_fft_estimate(srslte_ue_sl_t* q)
{
  if (q) {
    /* Run FFT for all subframe data */
    for (int j = 0; j < q->nof_rx_antennas; j++) {
      srslte_ofdm_rx_sf(&q->fft[j]);
    }
  } else {
    return SRSLTE_ERROR_INVALID_INPUTS;
  }
  return SRSLTE_SUCCESS;
}

/* Estimate PSCCH channel
 */
void estimate_pscch(srslte_ue_sl_t* q, uint32_t sub_channel_idx, uint32_t pscch_prb_start_idx, uint32_t cyclic_shift)
{
  srslte_chest_sl_cfg_t pscch_chest_sl_cfg;
  pscch_chest_sl_cfg.cyclic_shift  = cyclic_shift;
  pscch_chest_sl_cfg.prb_start_idx = pscch_prb_start_idx;
  srslte_chest_sl_set_cfg(&q->pscch_chest_rx[sub_channel_idx], pscch_chest_sl_cfg);
  srslte_chest_sl_ls_estimate_equalize(&q->pscch_chest_rx[sub_channel_idx], q->sf_symbols_rx[0], q->equalized_sf_buffer);
}

void estimate_pssch(srslte_ue_sl_t* q,
                    uint32_t sub_channel_idx,
                    srslte_sl_sf_cfg_t* sf,
                    uint32_t N_x_id,
                    uint32_t pssch_prb_start_idx,
                    uint32_t nof_prb_pssch)
{
  srslte_chest_sl_cfg_t pssch_chest_sl_cfg;
  pssch_chest_sl_cfg.N_x_id        = N_x_id;
  pssch_chest_sl_cfg.sf_idx        = sf->tti % 10;
  pssch_chest_sl_cfg.prb_start_idx = pssch_prb_start_idx;
  pssch_chest_sl_cfg.nof_prb       = nof_prb_pssch;
  srslte_chest_sl_set_cfg(&q->pssch_chest_rx[sub_channel_idx], pssch_chest_sl_cfg);
  srslte_chest_sl_ls_estimate_equalize(&q->pssch_chest_rx[sub_channel_idx], q->sf_symbols_rx[0], q->equalized_sf_buffer);
}

/* Decode PSCCH signal
 */
static int pscch_decode(srslte_ue_sl_t* q,
                        uint32_t sub_channel_idx,
                        uint32_t cyclic_shift,
                        uint32_t pscch_prb_start_idx,
                        srslte_ue_sl_res_t* sl_res)
{

  int ret = SRSLTE_ERROR_INVALID_INPUTS;

  if (q != NULL) {

    estimate_pscch(q, sub_channel_idx, pscch_prb_start_idx, cyclic_shift);

    uint8_t sci_rx[SRSLTE_SCI_MAX_LEN] = {};
    if (srslte_pscch_decode(&q->pscch_rx[sub_channel_idx], q->equalized_sf_buffer, sci_rx, pscch_prb_start_idx)) {
      DEBUG("Error decoding PSCCH (cyclic shift: %d, pscch_prb_start_idx: %d)\n", cyclic_shift, pscch_prb_start_idx);
      return SRSLTE_ERROR;
    } else {

      if (srslte_sci_format1_unpack(&q->sci_rx[sub_channel_idx], sci_rx)) {
        DEBUG("ERROR unpacking SCI Format 1 (cyclic shift: %d, pscch_prb_start_idx: %d)\n", cyclic_shift, pscch_prb_start_idx);
        return SRSLTE_ERROR;
      } else {
        q->sci_rx[sub_channel_idx].resource_reserv = srslte_intvl_from_reserv(q->sci_rx[sub_channel_idx].resource_reserv);
        sl_res->sci[sub_channel_idx] = q->sci_rx[sub_channel_idx];

        char sci_msg[SRSLTE_SCI_MSG_MAX_LEN] = {};
        srslte_sci_info(&q->sci_rx[sub_channel_idx], sci_msg, sizeof(sci_msg));
        INFO("%s", sci_msg);
      }
    }
    ret = SRSLTE_SUCCESS;
  }

  return ret;
}

/* Decode PSSCH signal
 */
static int pssch_decode(srslte_ue_sl_t* q,
                        srslte_sl_sf_cfg_t* sf,
                        uint32_t sub_channel_idx,
                        srslte_ue_sl_res_t* sl_res)
{
  int ret = SRSLTE_ERROR_INVALID_INPUTS;

  if (q != NULL) {
    ret = SRSLTE_ERROR;

    uint32_t sub_channel_start_idx = 0;
    uint32_t L_subCH               = 0;
    srslte_ra_sl_type0_from_riv(
        q->sci_rx[sub_channel_idx].riv, q->sl_comm_resource_pool.num_sub_channel, &L_subCH, &sub_channel_start_idx);

    // 3GPP TS 36.213 Section 14.1.1.4C
    uint32_t pssch_prb_start_idx = (sub_channel_idx * q->sl_comm_resource_pool.size_sub_channel) +
                                   q->pscch_rx[sub_channel_idx].pscch_nof_prb + q->sl_comm_resource_pool.start_prb_sub_channel;
    uint32_t nof_prb_pssch = ((L_subCH + sub_channel_idx) * q->sl_comm_resource_pool.size_sub_channel) -
                             pssch_prb_start_idx + q->sl_comm_resource_pool.start_prb_sub_channel;

    // make sure PRBs are valid for DFT precoding
    nof_prb_pssch = srslte_dft_precoding_get_valid_prb(nof_prb_pssch);

    uint32_t N_x_id = srslte_n_x_id_from_crc(q->pscch_rx[sub_channel_idx].sci_crc, SRSLTE_SCI_CRC_LEN);

    uint32_t rv_idx = 0;
    if (q->sci_rx[sub_channel_idx].retransmission == true) {
      rv_idx = 1;
    }

    estimate_pssch(q, sub_channel_idx, sf, N_x_id, pssch_prb_start_idx, nof_prb_pssch);

    srslte_pssch_cfg_t pssch_cfg = {
        pssch_prb_start_idx, nof_prb_pssch, N_x_id, q->sci_rx[sub_channel_idx].mcs_idx, rv_idx, sf->tti % 10};
    if (srslte_pssch_set_cfg(&q->pssch_rx[sub_channel_idx], pssch_cfg)) {
      ERROR("ERROR setting PSSCH config\n");
      ret = SRSLTE_ERROR;
    }

    DEBUG("PSSCH RX: prb_start_idx: %d, nof_prb: %d, N_x_id: %d, mcs_idx: %d, rv_idx: %d, sf_idx: %d\n",
          q->pssch_rx[sub_channel_idx].pssch_cfg.prb_start_idx,
          q->pssch_rx[sub_channel_idx].pssch_cfg.nof_prb,
          q->pssch_rx[sub_channel_idx].pssch_cfg.N_x_id,
          q->pssch_rx[sub_channel_idx].pssch_cfg.mcs_idx,
          q->pssch_rx[sub_channel_idx].pssch_cfg.rv_idx,
          q->pssch_rx[sub_channel_idx].pssch_cfg.sf_idx);


    if (srslte_pssch_decode(&q->pssch_rx[sub_channel_idx], q->equalized_sf_buffer, sl_res->data[sub_channel_idx], SRSLTE_SL_SCH_MAX_TB_LEN)) {
      DEBUG("Error decoding PSSCH\n");
      ret = SRSLTE_ERROR;
    } else {
      INFO("PSSCH decoding successfull\n");
      ret = SRSLTE_SUCCESS;
    }
  }
  return ret;
}

int srslte_ue_sl_decode_subch(srslte_ue_sl_t* q,
                              srslte_sl_sf_cfg_t* sf,
                              uint32_t sub_channel_idx,
                              srslte_ue_sl_res_t* sl_res)
{
  int ret = SRSLTE_ERROR;

  uint32_t pscch_prb_start_idx;
  if (q->sl_comm_resource_pool.adjacency_pscch_pssch) {
    pscch_prb_start_idx = sub_channel_idx * q->sl_comm_resource_pool.size_sub_channel;
  } else {
    pscch_prb_start_idx = sub_channel_idx * 2;
  }

  for (uint32_t cyclic_shift = 0; cyclic_shift <= 9; cyclic_shift += 3) {
    if (pscch_decode(q, sub_channel_idx, cyclic_shift, pscch_prb_start_idx, sl_res) == SRSLTE_SUCCESS) {
      if (pssch_decode(q, sf, sub_channel_idx, sl_res) == SRSLTE_SUCCESS) {
        ret = SRSLTE_SUCCESS;
      }
    }
  }
//  if (ret == SRSLTE_ERROR) {
//    printf("Error decoding PSCCH or PSSCH (sub_channel_idx: %d, pscch_prb_start_idx: %d)\n",
//           sub_channel_idx, pscch_prb_start_idx);
//  }

  return ret;
}
