#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: HackRF - RTLSDR loop back test
# Author: Aaron Scher
# Description: Transmit and receive example
# Generated: Sat Apr 18 09:07:08 2020
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import uhd
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.filter import pfb
from optparse import OptionParser
import epy_block_0
import numpy
import sip
import sys
import time
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self, hdr_format=digital.header_format_default(digital.packet_utils.default_access_code, 0), my_const=digital.constellation_calcdist((digital.psk_2()[0]), (digital.psk_2()[1]), 2, 1).base()):
        gr.top_block.__init__(self, "HackRF - RTLSDR loop back test")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("HackRF - RTLSDR loop back test")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Parameters
        ##################################################
        self.hdr_format = hdr_format
        self.my_const = my_const

        ##################################################
        # Variables
        ##################################################
        self.sps_TX = sps_TX = 40
        self.nfilts = nfilts = 32
        self.EBW = EBW = .35
        self.sps_RX = sps_RX = 40/10
        self.samp_rate = samp_rate = 240E3
        self.freq_offset_value = freq_offset_value = 30E3
        self.center_freq = center_freq = 430E6

        self.RRC_filter_taps = RRC_filter_taps = firdes.root_raised_cosine(nfilts, nfilts, 1.0, EBW, 5*sps_TX*nfilts)


        ##################################################
        # Blocks
        ##################################################
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	",".join(("", "")),
        	uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(0, 0)
        self.uhd_usrp_sink_0.set_gain(0, 0)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', '', False, False, '')
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win)
        self.pfb_arb_resampler_xxx_0 = pfb.arb_resampler_ccf(
        	  sps_TX,
                  taps=(RRC_filter_taps),
        	  flt_size=nfilts)
        self.pfb_arb_resampler_xxx_0.declare_sample_delay(0)

        self.epy_block_0 = epy_block_0.msg_block()
        self.digital_protocol_formatter_bb_0 = digital.protocol_formatter_bb(hdr_format, 'len_key')
        self.digital_diff_encoder_bb_0 = digital.diff_encoder_bb(2)
        self.digital_crc32_async_bb_1 = digital.crc32_async_bb(False)
        self.digital_chunks_to_symbols_xx_0_0 = digital.chunks_to_symbols_bc((my_const.points()), 1)
        self.digital_burst_shaper_xx_0 = digital.burst_shaper_cc((numpy.ones(500)), 4000, 4000, True, 'len_key')
        (self.digital_burst_shaper_xx_0).set_block_alias("burst_shaper0")
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, 'len_key', 0)
        self.blocks_tagged_stream_multiply_length_0 = blocks.tagged_stream_multiply_length(gr.sizeof_gr_complex*1, 'len_key', sps_TX)
        self.blocks_repack_bits_bb_0_0 = blocks.repack_bits_bb(8, my_const.bits_per_symbol(), 'len_key', False, gr.GR_MSB_FIRST)
        self.blocks_pdu_to_tagged_stream_1 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'len_key')
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.5, ))
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, freq_offset_value, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.digital_crc32_async_bb_1, 'out'), (self.blocks_pdu_to_tagged_stream_1, 'pdus'))
        self.msg_connect((self.epy_block_0, 'msg_out'), (self.digital_crc32_async_bb_1, 'in'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.epy_block_0, 'msg_in'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_1, 0), (self.blocks_tagged_stream_mux_0, 1))
        self.connect((self.blocks_pdu_to_tagged_stream_1, 0), (self.digital_protocol_formatter_bb_0, 0))
        self.connect((self.blocks_repack_bits_bb_0_0, 0), (self.digital_diff_encoder_bb_0, 0))
        self.connect((self.blocks_tagged_stream_multiply_length_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.blocks_repack_bits_bb_0_0, 0))
        self.connect((self.digital_burst_shaper_xx_0, 0), (self.pfb_arb_resampler_xxx_0, 0))
        self.connect((self.digital_chunks_to_symbols_xx_0_0, 0), (self.digital_burst_shaper_xx_0, 0))
        self.connect((self.digital_diff_encoder_bb_0, 0), (self.digital_chunks_to_symbols_xx_0_0, 0))
        self.connect((self.digital_protocol_formatter_bb_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.pfb_arb_resampler_xxx_0, 0), (self.blocks_tagged_stream_multiply_length_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_hdr_format(self):
        return self.hdr_format

    def set_hdr_format(self, hdr_format):
        self.hdr_format = hdr_format

    def get_my_const(self):
        return self.my_const

    def set_my_const(self, my_const):
        self.my_const = my_const

    def get_sps_TX(self):
        return self.sps_TX

    def set_sps_TX(self, sps_TX):
        self.sps_TX = sps_TX
        self.pfb_arb_resampler_xxx_0.set_rate(self.sps_TX)
        self.blocks_tagged_stream_multiply_length_0.set_scalar(self.sps_TX)

    def get_nfilts(self):
        return self.nfilts

    def set_nfilts(self, nfilts):
        self.nfilts = nfilts

    def get_EBW(self):
        return self.EBW

    def set_EBW(self, EBW):
        self.EBW = EBW

    def get_sps_RX(self):
        return self.sps_RX

    def set_sps_RX(self, sps_RX):
        self.sps_RX = sps_RX

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)

    def get_freq_offset_value(self):
        return self.freq_offset_value

    def set_freq_offset_value(self, freq_offset_value):
        self.freq_offset_value = freq_offset_value
        self.analog_sig_source_x_0.set_frequency(self.freq_offset_value)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq

    def get_RRC_filter_taps(self):
        return self.RRC_filter_taps

    def set_RRC_filter_taps(self, RRC_filter_taps):
        self.RRC_filter_taps = RRC_filter_taps
        self.pfb_arb_resampler_xxx_0.set_taps((self.RRC_filter_taps))


def argument_parser():
    description = 'Transmit and receive example'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    return parser


def main(top_block_cls=top_block, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
