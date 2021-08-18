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

#include <signal.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <strings.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "srslte/phy/common/phy_common_sl.h"
#include "srslte/phy/phch/pssch.h"
#include "srslte/phy/phch/sci.h"
#include "srslte/phy/rf/rf.h"
#include "srslte/phy/ue/ue_sync.h"
#include "srslte/phy/utils/debug.h"
#include "srslte/phy/utils/random.h"
#include "srslte/phy/utils/vector.h"
#include "srslte/phy/ue/ue_sl.h"


#define REP_INTERVL 100

bool keep_running = true;
bool debug_log = false;
srslte_cell_sl_t cell_sl = {.nof_prb = 50, .tm = SRSLTE_SIDELINK_TM4, .cp = SRSLTE_CP_NORM, .N_sl_id = 19};

typedef struct {
  bool   use_standard_lte_rates;
  char*  input_file_name;
  char*  log_file_name;
  char*  rf_dev;
  char*  rf_args;
  double rf_freq;
  float  rf_gain;

  // Sidelink specific args
  uint32_t num_sub_channel;
  uint32_t sub_channel_start_idx;
  uint32_t mcs_idx;
  uint32_t l_sub_channel;
} prog_args_t;

typedef struct {
  uint32_t sub_channel_start_idx;
  uint32_t l_sub_channel;
} sf_config_t;

typedef struct {
  char sci_msg[SRSLTE_SCI_MSG_MAX_LEN];
  uint32_t pssch_prb_start_idx;
  uint32_t pssch_nof_prb;
  uint32_t pssch_N_x_id;
  uint32_t pssch_mcs_idx;
  uint32_t pssch_rv_idx;
  uint32_t sf_idx;
} tx_metrics_t;

void args_default(prog_args_t* args)
{
  args->use_standard_lte_rates = false;
  args->input_file_name        = NULL;
  args->log_file_name          = NULL;
  args->rf_dev                 = "";
  args->rf_args                = "";
  args->rf_freq                = 5.92e9;
  args->rf_gain                = 80;
  args->num_sub_channel        = 10;
  args->mcs_idx                = 20;
  args->sub_channel_start_idx  = 0;
  args->l_sub_channel          = 2;
}

void sig_int_handler(int signo)
{
  fprintf(stdout, "SIGINT received. Exiting...\n");
  fflush(stdout);
  if (signo == SIGINT) {
    keep_running = false;
  } else if (signo == SIGSEGV) {
    exit(1);
  }
}

void usage(prog_args_t* args, char* prog)
{
  fprintf(stdout, "Usage: %s [acdgilmnoprs] -f tx_frequency_hz -v verbose\n", prog);
  fprintf(stdout, "\t-a RF args [Default %s]\n", args->rf_args);
  fprintf(stdout, "\t-c N_sl_id [Default %d]\n", cell_sl.N_sl_id);
  fprintf(stdout, "\t-d RF devicename [Default %s]\n", args->rf_dev);
  fprintf(stdout, "\t-g RF Gain [Default %.2f dB]\n", args->rf_gain);
  fprintf(stdout, "\t-i input_file_name for csv file containing sub_channel_start_idx and l_sub_channel.\n");
  fprintf(stdout, "\t-l l_sub_channel [Default %d]. If input_file_name is specified this will be ignored.\n", args->l_sub_channel);
  fprintf(stdout, "\t-m mcs_idx [Default %d]\n", args->mcs_idx);
  fprintf(stdout, "\t-n num_sub_channel [Default for 50 prbs %d]\n", args->num_sub_channel);
  fprintf(stdout, "\t-o log_file_name.\n");
  fprintf(stdout, "\t-p nof_prb [Default %d]\n", cell_sl.nof_prb);
  fprintf(stdout, "\t-r use_standard_lte_rates [Default %i]\n", args->use_standard_lte_rates);
  fprintf(stdout, "\t-s sub_channel_start_idx [Default %d]. If input_file_name is specified this will be ignored.\n", args->sub_channel_start_idx);
  fflush(stdout);
}

void parse_args(prog_args_t* args, int argc, char** argv)
{
  int opt;
  args_default(args);

  while ((opt = getopt(argc, argv, "acdfgilmnoprsv")) != -1) {
    switch (opt) {
      case 'a':
        args->rf_args = argv[optind];
        break;
      case 'c':
        cell_sl.N_sl_id = (int32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'd':
        args->rf_dev = argv[optind];
        break;
      case 'f':
        args->rf_freq = strtof(argv[optind], NULL);
        break;
      case 'g':
        args->rf_gain = strtof(argv[optind], NULL);
        break;
      case 'i':
        args->input_file_name = argv[optind];
        break;
      case 'l':
        args->l_sub_channel = (uint32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'm':
        args->mcs_idx = (uint32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'n':
        args->num_sub_channel = (uint32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'o':
        args->log_file_name = argv[optind];
        break;
      case 'p':
        cell_sl.nof_prb = (int32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'r':
        args->use_standard_lte_rates = true;
        break;
      case 's':
        args->sub_channel_start_idx = (uint32_t)strtol(argv[optind], NULL, 10);
        break;
      case 'v':
        debug_log = true;
        break;

      default:
        usage(args, argv[0]);
        exit(-1);
    }
  }
  if (SRSLTE_CP_ISEXT(cell_sl.cp) && cell_sl.tm >= SRSLTE_SIDELINK_TM3) {
    ERROR("Selected TM does not support extended CP");
    usage(args, argv[0]);
    exit(-1);
  }
}

void parse_input_file(char* filename, sf_config_t sf_config[REP_INTERVL], uint32_t num_subchannel)
{
  FILE *input_file;
  input_file = fopen(filename, "r");
  if (input_file == NULL) {
    ERROR("Error reading file\n");
    exit(1);
  }

  //read and ignore header line
  char buffer[100];
  fgets(buffer, 100, input_file);

  for (int line = 0; line < REP_INTERVL; line++) {
    if (EOF == fscanf(input_file, "%d,%d", &sf_config[line].sub_channel_start_idx, &sf_config[line].l_sub_channel)) {
      if (line < REP_INTERVL - 1) {
        ERROR("File to short. 100 lines expected but only %d lines were found\n", line);
        exit(1);
      }
    }
    if (sf_config[line].sub_channel_start_idx + sf_config[line].l_sub_channel > num_subchannel) {
      ERROR("Invalid configuration in line %d: sub_channel_start_idx=%d, l_sub_channel=%d."
            "Configration exceeds number of subchannels (%d).\n",
            line, sf_config[line].sub_channel_start_idx, sf_config[line].l_sub_channel, num_subchannel);
      exit(1);
    }
    if (debug_log) {
      fprintf(stdout, "[%d] sub_channel_start_idx=%d, l_sub_channel=%d\n",
              line, sf_config[line].sub_channel_start_idx, sf_config[line].l_sub_channel);
      fflush(stdout);
    }
  }

  fclose(input_file);
}

void write_tx_metrics(srslte_ue_sl_t* srsue_vue_sl, tx_metrics_t* tx_metrics, uint32_t sf_idx)
{
  srslte_sci_info(&srsue_vue_sl->sci_tx, tx_metrics->sci_msg, sizeof(tx_metrics->sci_msg));

  tx_metrics->pssch_prb_start_idx = srsue_vue_sl->pssch_tx.pssch_cfg.prb_start_idx;
  tx_metrics->pssch_nof_prb = srsue_vue_sl->pssch_tx.pssch_cfg.nof_prb;
  tx_metrics->pssch_N_x_id = srsue_vue_sl->pssch_tx.pssch_cfg.N_x_id;
  tx_metrics->pssch_mcs_idx = srsue_vue_sl->pssch_tx.pssch_cfg.mcs_idx;
  tx_metrics->pssch_rv_idx = srsue_vue_sl->pssch_tx.pssch_cfg.rv_idx;
  tx_metrics->sf_idx = sf_idx;
}

void print_tx_metrics(tx_metrics_t* tx_metrics)
{
  fprintf(stdout, "%s", tx_metrics->sci_msg);
  fprintf(stdout, "PSSCH: prb_start_idx: %d, nof_prb: %d, N_x_id: %d, mcs_idx: %d, rv_idx: %d, sf_idx: %d\n",
         tx_metrics->pssch_prb_start_idx,
         tx_metrics->pssch_nof_prb,
         tx_metrics->pssch_N_x_id,
         tx_metrics->pssch_mcs_idx,
         tx_metrics->pssch_rv_idx,
         tx_metrics->sf_idx % 10);
  fflush(stdout);
}

void get_start_time(srslte_rf_t* rf, srslte_timestamp_t* t)
{
  uint32_t start_time_full_ms;
  double   start_time_frac_ms;

  srslte_rf_get_time(rf, &t->full_secs, &t->frac_secs);

  fprintf(stdout, "start time: %f\n", srslte_timestamp_real(t));
  fflush(stdout);

  // make sure the fractional transmit time is ms-aligned
  start_time_full_ms = floor(t->frac_secs * 1e3);
  start_time_frac_ms = t->frac_secs - (start_time_full_ms / 1e3);
  if (start_time_frac_ms > 0.0) {
    srslte_timestamp_sub(t, 0, start_time_frac_ms);
  }
  // Add computing-time offset
  srslte_timestamp_add(t, 0, 3 * 1e-3);
}


int main(int argc, char** argv)
{
  signal(SIGINT, sig_int_handler);
  sigset_t sigset;
  sigemptyset(&sigset);
  sigaddset(&sigset, SIGINT);
  sigprocmask(SIG_UNBLOCK, &sigset, NULL);

  prog_args_t prog_args;
  parse_args(&prog_args, argc, argv);

  /***** logfile *******/
  struct tm* timeinfo;
  time_t     current_time = time(0); // Get the system time
  timeinfo                = localtime(&current_time);

  FILE *logfile;
  if (prog_args.log_file_name) {
    logfile = fopen(prog_args.log_file_name, "w");
    fprintf(stdout, "writing logfile: %s\n", prog_args.log_file_name);
    fflush(stdout);
  } else {

    const char * home = getenv("HOME");
    const char * subPath = "/v2x_tg_logfiles";
    char * path = (char*)malloc(strlen(home) + strlen(subPath) + 1);
    strcpy(path, home);
    strcat(path, subPath);

    mkdir(path, 0700);
    char filename[100];

    sprintf(filename,
            "%s/v2x_tg_%d_%d_%d-%d_%d_%d.csv",
            path,
            timeinfo->tm_year + 1900,
            timeinfo->tm_mon + 1,
            timeinfo->tm_mday,
            timeinfo->tm_hour,
            timeinfo->tm_min,
            timeinfo->tm_sec);

    logfile = fopen(filename, "w");

    fprintf(stdout, "writing logfile: %s\n", filename);
    fflush(stdout);

    free(path);
  }

  // write header
  fprintf(logfile, "tx_timestamp_us,prb_start_idx,nof_prb,N_x_id,mcs_idx,rv_idx,sf_idx\n");

  /***** Init *******/
  tx_metrics_t tx_metrics[REP_INTERVL] = {};

  sf_config_t sf_config[REP_INTERVL] = {};
  // if input_file_name is specified, read values from file, else use prog_args values
  if (prog_args.input_file_name) {
    fprintf(stdout, "Reading input file %s\n", prog_args.input_file_name);
    fflush(stdout);
    parse_input_file(prog_args.input_file_name, sf_config, prog_args.num_sub_channel);
  } else {
    for (int sf_idx = 0; sf_idx < REP_INTERVL; sf_idx++) {
      sf_config[sf_idx].sub_channel_start_idx = prog_args.sub_channel_start_idx;
      sf_config[sf_idx].l_sub_channel = prog_args.l_sub_channel;
    }
  }

  srslte_use_standard_symbol_size(prog_args.use_standard_lte_rates);

  srslte_sl_comm_resource_pool_t sl_comm_resource_pool;

  // init resource pool
  if (srslte_sl_comm_resource_pool_set_cfg(&sl_comm_resource_pool, cell_sl, prog_args.num_sub_channel, 0, true) != SRSLTE_SUCCESS) {
    ERROR("Error initializing sl_comm_resource_pool\n");
    return SRSLTE_ERROR;
  }

  srslte_rf_t radio;
  fprintf(stdout, "Opening RF device...\n");
  fflush(stdout);
  if (srslte_rf_open(&radio, prog_args.rf_args)) {
    ERROR("Error opening rf\n");
    exit(-1);
  }

  fprintf(stdout, "Set TX freq: %.6f MHz\n",
         srslte_rf_set_tx_freq(&radio, 0, prog_args.rf_freq) / 1e6);
  fprintf(stdout, "Set TX gain: %.1f dB\n", srslte_rf_set_tx_gain(&radio, prog_args.rf_gain));
  fflush(stdout);

  int srate = srslte_sampling_freq_hz(cell_sl.nof_prb);
  if (srate != -1) {
    fprintf(stdout, "Setting sampling rate %.2f MHz\n", (float)srate / 1000000);
    fflush(stdout);
    float srate_rf = srslte_rf_set_tx_srate(&radio, (double)srate);
    if (srate_rf != srate) {
      ERROR("Could not set sampling rate\n");
      exit(-1);
    }
  } else {
    ERROR("Invalid number of PRB %d\n", cell_sl.nof_prb);
    exit(-1);
  }
  sleep(1);

  srslte_ue_sl_t srsue_vue_sl;
  srslte_ue_sl_init(&srsue_vue_sl, cell_sl, sl_comm_resource_pool, 0);

  /***** prepare TX data *******/
  srslte_set_sci(&srsue_vue_sl.sci_tx, 1, REP_INTERVL, 0, false, 0, 4);

  // Randomize tx data to fill the transport block
  // Transport block buffer
  uint8_t tb[SRSLTE_SL_SCH_MAX_TB_LEN] = {};
  struct timeval tv;
  gettimeofday(&tv, NULL);
  srslte_random_t random_gen = srslte_random_init(tv.tv_usec);
  for (int i = 0; i < srsue_vue_sl.pssch_tx.sl_sch_tb_len; i++) {
    tb[i] = srslte_random_uniform_int_dist(random_gen, 0, 1);
  }

  srslte_pssch_data_t data;
  data.ptr = tb;

  srslte_sl_sf_cfg_t sf;
  cf_t* signal_buffer_tx[REP_INTERVL] = {};

  fprintf(stdout, "creating signal buffers...\n");
  fflush(stdout);
  for (int sf_idx = 0; sf_idx < REP_INTERVL; sf_idx++) {

    if (sf_config[sf_idx].l_sub_channel > 0) {
      if (debug_log) {
        fprintf(stdout, "signal_buffer %d\n", sf_idx);
        fflush(stdout);
      }
      signal_buffer_tx[sf_idx] = srslte_vec_cf_malloc(srsue_vue_sl.sf_len);
      if (!signal_buffer_tx[sf_idx]) {
        perror("malloc");
        exit(-1);
      }

      data.sub_channel_start_idx = sf_config[sf_idx].sub_channel_start_idx;
      data.l_sub_channel         = sf_config[sf_idx].l_sub_channel;

      sf.tti = sf_idx;
      if (srslte_ue_sl_encode(&srsue_vue_sl, &sf, &data)) {
        ERROR("Error encoding sidelink\n");
        exit(-1);
      }

      write_tx_metrics(&srsue_vue_sl, &tx_metrics[sf_idx], sf_idx);

      memcpy(signal_buffer_tx[sf_idx], srsue_vue_sl.signal_buffer_tx, sizeof(cf_t) * srsue_vue_sl.sf_len);
    }
  }

  /***** timing *******/
  srslte_timestamp_t start_time, tx_time, now;

  get_start_time(&radio, &start_time);

  uint32_t tx_sec_offset = 0;
  uint32_t tx_msec_offset = 0;

  while (keep_running) {

    srslte_timestamp_copy(&tx_time, &start_time);
    srslte_timestamp_add(&tx_time, tx_sec_offset, tx_msec_offset * 1e-3);

    srslte_rf_get_time(&radio, &now.full_secs, &now.frac_secs);

    // if tx_time is in the past reset time
    if (srslte_timestamp_uint64(&now, srate) > srslte_timestamp_uint64(&tx_time, srate)) {
      ERROR("tx_time is in the past (tx_time: %f, now: %f). Setting new start time.\n",
            srslte_timestamp_real(&tx_time), srslte_timestamp_real(&now));
      get_start_time(&radio, &start_time);

      tx_sec_offset = 0;
      tx_msec_offset = 0;
    }
    else {

      // only if data to transmit
      if (sf_config[tx_msec_offset % REP_INTERVL].l_sub_channel > 0) {

        int ret = srslte_rf_send_timed2(&radio,
                                        signal_buffer_tx[tx_msec_offset % REP_INTERVL],
                                        srsue_vue_sl.sf_len,
                                        tx_time.full_secs,
                                        tx_time.frac_secs,
                                        true,
                                        true);
        if (ret < 0) {
          ERROR("Error sending data: %d\n", ret);
        }

        // write logfile
        fprintf(logfile,"%lu,%d,%d,%d,%d,%d,%d\n",
                (uint64_t) round(srslte_timestamp_real(&tx_time) * 1e6),
                tx_metrics->pssch_prb_start_idx,
                tx_metrics->pssch_nof_prb,
                tx_metrics->pssch_N_x_id,
                tx_metrics->pssch_mcs_idx,
                tx_metrics->pssch_rv_idx,
                tx_metrics->sf_idx % 10);

        if (debug_log) {
          print_tx_metrics(&tx_metrics[tx_msec_offset % REP_INTERVL]);
        }
      }

      tx_msec_offset++;
      if (tx_msec_offset == 1000) {
        tx_sec_offset++;
        tx_msec_offset = 0;
      }
    }

  }

  fclose(logfile);

  srslte_rf_close(&radio);
  srslte_ue_sl_free(&srsue_vue_sl);

  for (int i = 0; i < REP_INTERVL; i++) {
    free(signal_buffer_tx[i]);
  }

  return SRSLTE_SUCCESS;
}