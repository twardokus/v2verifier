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

/******************************************************************************
 *  File:         ue_sl.h
 *
 *  Description:  UE sidelink object.
 *
 *                This module is a frontend to all the sidelink data and control
 *                channel processing modules.
 *
 *  Reference:
 *****************************************************************************/

#ifndef SRSLTE_UE_SL_H
#define SRSLTE_UE_SL_H

#include "srslte/phy/ch_estimation/chest_sl.h"
#include "srslte/phy/common/phy_common.h"
#include "srslte/phy/dft/ofdm.h"
#include "srslte/phy/phch/dci.h"
#include "srslte/phy/phch/pscch.h"
#include "srslte/phy/phch/pssch.h"
#include "srslte/phy/phch/ra_sl.h"
#include "srslte/phy/phch/sci.h"
#include "srslte/phy/sync/cfo.h"
#include "srslte/phy/utils/debug.h"
#include "srslte/phy/utils/vector.h"

#include "srslte/config.h"

typedef struct SRSLTE_API {
  srslte_cell_sl_t cell;

  srslte_sl_comm_resource_pool_t sl_comm_resource_pool;

  srslte_ofdm_t fft[SRSLTE_MAX_PORTS];
  srslte_ofdm_t ifft;

  srslte_chest_sl_t pscch_chest_tx;
  srslte_chest_sl_t pssch_chest_tx;
  srslte_chest_sl_t pscch_chest_rx[SRSLTE_MAX_NUM_SUB_CHANNEL];
  srslte_chest_sl_t pssch_chest_rx[SRSLTE_MAX_NUM_SUB_CHANNEL];

  srslte_sci_t sci_rx[SRSLTE_MAX_NUM_SUB_CHANNEL];
  srslte_sci_t sci_tx;

  srslte_pscch_t pscch_tx;
  srslte_pssch_t pssch_tx;
  srslte_pscch_t pscch_rx[SRSLTE_MAX_NUM_SUB_CHANNEL];
  srslte_pssch_t pssch_rx[SRSLTE_MAX_NUM_SUB_CHANNEL];

  cf_t* signal_buffer_tx;
  cf_t* sf_symbols_tx;
  cf_t* signal_buffer_rx[SRSLTE_MAX_CHANNELS];
  cf_t* sf_symbols_rx[SRSLTE_MAX_PORTS];
  cf_t* equalized_sf_buffer;

  uint32_t nof_rx_antennas;
  uint32_t sf_len;
  uint32_t sf_n_re;

} srslte_ue_sl_t;

typedef struct SRSLTE_API {
  srslte_sci_t sci[SRSLTE_MAX_NUM_SUB_CHANNEL];
  uint8_t*     data[SRSLTE_MAX_NUM_SUB_CHANNEL];
} srslte_ue_sl_res_t;

SRSLTE_API int srslte_ue_sl_init(srslte_ue_sl_t* q,
                                 srslte_cell_sl_t cell,
                                 srslte_sl_comm_resource_pool_t sl_comm_resource_pool,
                                 uint32_t nof_rx_antennas);

SRSLTE_API void srslte_ue_sl_free(srslte_ue_sl_t* q);

SRSLTE_API int srslte_ue_sl_set_cell(srslte_ue_sl_t* q, srslte_cell_sl_t cell);

SRSLTE_API int srslte_ue_sl_set_sl_comm_resource_pool(srslte_ue_sl_t* q, srslte_sl_comm_resource_pool_t sl_comm);

SRSLTE_API uint32_t srslte_n_x_id_from_crc(uint8_t *crc, uint32_t crc_len);

SRSLTE_API void srslte_set_sci(srslte_sci_t* sci,
                               uint32_t priority,
                               uint32_t resource_reserv_itvl,
                               uint32_t time_gap,
                               bool     retransmission,
                               uint32_t transmission_format,
                               uint32_t mcs_idx);

SRSLTE_API void srslte_set_sci_riv(srslte_ue_sl_t* q,
                                   uint32_t sub_channel_start_idx,
                                   uint32_t l_sub_channel);

SRSLTE_API int srslte_ue_sl_encode(srslte_ue_sl_t* q,
                                   srslte_sl_sf_cfg_t* sf,
                                   srslte_pssch_data_t* data);

SRSLTE_API int srslte_ue_sl_decode_fft_estimate(srslte_ue_sl_t* q);

SRSLTE_API int srslte_ue_sl_decode_subch(srslte_ue_sl_t* q,
                                         srslte_sl_sf_cfg_t* sf,
                                         uint32_t sub_channel_idx,
                                         srslte_ue_sl_res_t* sl_res);


#endif // SRSLTE_UE_SL_H
