import math

MCS = {
    0: [6, 6],
    1: [9, 6],
    2: [12, 12],
    3: [18, 12],
    4: [24, 24],
    5: [36, 24],
    6: [48, 24],
    7: [54, 24],
}


class Times:

    t_slot = 9  # [us]
    t_sifs = 16  # [us]
    t_difs = 3 * t_slot + t_sifs  # [us]
    ack_timeout = 45  # [us]

    # Mac overhead
    mac_overhead = 40 * 8  # [b]

    # ACK size
    ack_size = 14 * 8  # [b]

    # overhead
    _overhead = 22  # [b]

    def __init__(self, payload: int = 1472, mcs: int = 7):
        self.payload = payload
        self.mcs = mcs
        # OFDM parameters
        self.phy_data_rate = MCS[mcs][0] * pow(
            10, -6
        )  # [Mb/us] Possible values 6, 9, 12, 18, 24, 36, 48, 54
        self.phy_ctr_rate = MCS[mcs][1] * pow(10, -6)  # [Mb/u]
        self.n_data = 4 * self.phy_data_rate  # [b/symbol]
        self.n_ctr = 4 * self.phy_ctr_rate  # [b/symbol]
        self.data_rate = MCS[mcs][0]  # [b/us]
        self.ctr_rate = MCS[mcs][1]  # [b/us]

        self.ofdm_preamble = 16  # [us]
        self.ofdm_signal = 24 / self.ctr_rate  # [us]

    # Data frame time
    def get_ppdu_frame_time(self):
        msdu = self.payload * 8  # [b]
        # MacFrame
        mac_frame = Times.mac_overhead + msdu  # [b]
        # PPDU Padding
        ppdu_padding = math.ceil(
            (Times._overhead + mac_frame) / self.n_data
        ) * self.n_data - (Times._overhead + mac_frame)
        # CPSDU Frame
        cpsdu = Times._overhead + mac_frame + ppdu_padding  # [b]
        # PPDU Frame
        ppdu = self.ofdm_preamble + self.ofdm_signal + cpsdu / self.data_rate  # [us]
        ppdu_tx_time = math.ceil(ppdu)
        return ppdu_tx_time  # [us]

    # ACK frame time with SIFS
    def get_ack_frame_time(self):
        ack = Times._overhead + Times.ack_size  # [b]
        ack = self.ofdm_preamble + self.ofdm_signal + ack / self.ctr_rate  # [us]
        ack_tx_time = Times.t_sifs + ack
        # return math.ceil(ack_tx_time)  # [us]
        return 44

    # # ACK Timeout
    # def get_ack_timeout():
    #     return ack_timeout

    def get_thr(self):
        return (self.payload * 8) / (
            self.get_ppdu_frame_time() + self.get_ack_frame_time() + Times.t_difs
        )