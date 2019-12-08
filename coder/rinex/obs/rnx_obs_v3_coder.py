#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
#
# @author kangao
# @since 2019/11/23

from coder.rinex.rnx_coder import RNXCoder
from coder.rinex.rnx_coder import RNXHeader
from coder.rinex.obs.obs_type import ObsType
from coder.sat_id import SatID
from time.civil_time import CivilTime
from coord.position import Cartesian
from coord.triple import Triple
import time.time_system as time_system
from coder.rinex import rnx_const
import coder.satellite_system as satellite_system


class RNXObsV3Coder(RNXCoder):

    def __init__(self, ds):
        super(RNXObsV3Coder, self).__init__(ds)
        self.__obs_v3_header = None

    def read_header(self):
        if self.__obs_v3_header:
            return self.__obs_v3_header
        self.__obs_v3_header = RNXObsV3Header()
        self.__obs_v3_header.read(self.data_source)
        return self.__obs_v3_header

    def read_epoch(self):
        obs_v3_epoch = RNXObsV3Epoch(self.read_header().sys_obs_types)
        if obs_v3_epoch.read(self.data_source):
            return obs_v3_epoch
        else:
            return None

    def write_header(self, header):
        if not isinstance(header, RNXObsV3Header):
            raise Exception('header must be RNXObsV3Header.')
        header.write(self.data_source)

    def write_epoch(self, epoch):
        pass


class RNXObsV3Header(RNXHeader):

    def __init__(self):
        super(RNXObsV3Header, self).__init__()
        self.marker_name = None
        self.marker_number = None
        self.marker_type = None
        self.observer = None
        self.agency = None
        self.recv_number = None
        self.recv_type = None
        self.recv_vers = None
        self.ant_number = None
        self.ant_type = None
        self.approx_position = None
        self.ant_delta_hen = None
        self.ant_delta_xyz = None
        self.ant_phase_center = None
        self.ant_sight_xyz = None
        self.ant_zero_dir_azi = None
        self.ant_zero_dir_xyz = None
        self.center_of_mass = None
        self.sys_obs_types = None
        self.signal_strength_unit = None
        self.interval = None
        self.time_of_first_obs = None
        self.time_of_last_obs = None
        self.rcv_clock_offs_applied = None
        self.sys_dcbs_applied = None
        self.sys_pcvs_applied = None
        self.sys_scale_factor = None
        self.sys_phase_shift = None
        self.glo_slot_and_frq = None
        self.glo_cod_phs_bis = None
        self.leap_second = None
        self.number_of_satellite = None

    def _init_handler_map(self):
        self._read_handler_map[rnx_const.__MARKER_NAME__] = self.__read_marker_name
        self._read_handler_map[rnx_const.__MARKER_NUMBER__] = self.__read_marker_number
        self._read_handler_map[rnx_const.__MARKER_TYPE__] = self.__read_marker_type
        self._read_handler_map[rnx_const.__OBSERVER_AGENCY__] = self.__read_observer_agency
        self._read_handler_map[rnx_const.__REC_TYPE_VERS__] = self.__read_rec_type_vers
        self._read_handler_map[rnx_const.__ANT_TYPE__] = self.__read_ant_type
        self._read_handler_map[rnx_const.__APPROX_POSITION_XYZ__] = self.__read_approx_position
        self._read_handler_map[rnx_const.__ANT_DELTA_H_E_N__] = self.__read_ant_delta_hen
        self._read_handler_map[rnx_const.__ANT_DELTA_X_Y_Z__] = self.__read_ant_delta_xyz
        self._read_handler_map[rnx_const.__ANT_PHASE_CENTER__] = self.__read_ant_phase_center
        self._read_handler_map[rnx_const.__ANT_B_SIGHT_X_Y_Z__] = self.__read_ant_sight_xyz
        self._read_handler_map[rnx_const.__ANT_ZERODIR_AZI__] = self.__read_ant_zerodir_azi
        self._read_handler_map[rnx_const.__ANT_ZERODIR_XYZ__] = self.__read_ant_zerodir_xyz
        self._read_handler_map[rnx_const.__CENTER_OF_MASS_XYZ__] = self.__read_center_of_mass_xyz
        self._read_handler_map[rnx_const.__SYS_OBS_TYPES__] = self.__read_sys_obs_types
        self._read_handler_map[rnx_const.__SIGNAL_STRENGTH_UNIT__] = self.__read_signal_strength_unit
        self._read_handler_map[rnx_const.__INTERVAL__] = self.__read_interval
        self._read_handler_map[rnx_const.__TIME_OF_FIRST_OBS__] = self.__read_time_of_first_obs
        self._read_handler_map[rnx_const.__TIME_OF_LAST_OBS__] = self.__read_time_of_last_obs
        self._read_handler_map[rnx_const.__RCV_CLOCK_OFFS_APPL__] = self.__read_rcv_clock_offs_applied
        self._read_handler_map[rnx_const.__SYS_DCBS_APPLIED__] = self.__read_sys_dcbs_applied
        self._read_handler_map[rnx_const.__SYS_PCVS_APPLIED__] = self.__read_sys_pcvs_applied
        self._read_handler_map[rnx_const.__SYS_SCALE_FACTOR__] = self.__read_sys_scale_factor
        self._read_handler_map[rnx_const.__SYS_PHASE_SHIFT__] = self.__read_sys_phase_shift
        self._read_handler_map[rnx_const.__GLONASS_SLOT_FRQ__] = self.__read_glo_slot_and_frq
        self._read_handler_map[rnx_const.__GLONASS_COD_PHS_BIS__] = self.__read_glo_cod_phs_bis
        self._read_handler_map[rnx_const.__OF_SATELLITES__] = self.__read_number_of_satellite
        self._write_handler_list.append(self.__write_marker_name)
        self._write_handler_list.append(self.__write_marker_number)
        self._write_handler_list.append(self.__write_marker_type)
        self._write_handler_list.append(self.__write_observer_agency)
        self._write_handler_list.append(self.__write_rec_type_vers)
        self._write_handler_list.append(self.__write_ant_type)
        self._write_handler_list.append(self.__write_approx_position)
        self._write_handler_list.append(self.__write_ant_delta_hen)
        self._write_handler_list.append(self.__write_ant_delta_xyz)
        self._write_handler_list.append(self.__write_ant_phase_center)
        self._write_handler_list.append(self.__write_ant_sight_xyz)
        self._write_handler_list.append(self.__write_ant_zerodir_azi)
        self._write_handler_list.append(self.__write_ant_zerodir_xyz)
        self._write_handler_list.append(self.__write_center_of_mass_xyz)
        self._write_handler_list.append(self.__write_sys_obs_types)
        self._write_handler_list.append(self.__write_signal_strength_unit)
        self._write_handler_list.append(self.__write_interval)
        self._write_handler_list.append(self.__write_time_of_first_obs)
        self._write_handler_list.append(self.__write_time_of_last_obs)
        self._write_handler_list.append(self.__write_rcv_clock_offs_applied)
        self._write_handler_list.append(self.__write_sys_dcbs_applied)
        self._write_handler_list.append(self.__write_sys_pcvs_applied)
        self._write_handler_list.append(self.__write_sys_scale_factor)
        self._write_handler_list.append(self.__write_sys_phase_shift)
        self._write_handler_list.append(self.__write_glo_slot_and_frq)
        self._write_handler_list.append(self.__write_glo_cod_phs_bis)
        self._write_handler_list.append(self.__write_number_of_satellite)
        super(RNXObsV3Header, self)._init_handler_map()

    def __read_marker_name(self, ds, line):
        self.marker_name = line[0:60]
        return True

    def __write_marker_name(self, ds):
        pass

    def __read_marker_number(self, ds, line):
        self.marker_number = line[0:20]
        return True

    def __write_marker_number(self, ds):
        pass

    def __read_marker_type(self, ds, line):
        self.marker_type = line[0:20]
        return True

    def __write_marker_type(self, ds):
        pass

    def __read_observer_agency(self, ds, line):
        self.observer = line[0:20]
        self.agency = line[20:60]
        return True

    def __write_observer_agency(self, ds):
        pass

    def __read_rec_type_vers(self, ds, line):
        self.recv_number = line[0:20]
        self.recv_type = line[20:40]
        self.recv_vers = line[40:60]
        return True

    def __write_rec_type_vers(self, ds):
        pass

    def __read_ant_type(self, ds, line):
        self.ant_number = line[0:20]
        self.ant_type = line[20:40]
        return True

    def __write_ant_type(self, ds):
        pass

    def __read_approx_position(self, ds, line):
        if not self.approx_position:
            self.approx_position = Cartesian()
        self.approx_position[0] = float(line[0:14])
        self.approx_position[1] = float(line[14:28])
        self.approx_position[2] = float(line[28:42])
        return True

    def __write_approx_position(self, ds):
        pass

    def __read_ant_delta_hen(self, ds, line):
        if not self.ant_delta_hen:
            self.ant_delta_hen = Triple()
        self.ant_delta_hen[0] = float(line[0:14])
        self.ant_delta_hen[1] = float(line[14:28])
        self.ant_delta_hen[2] = float(line[28:42])
        return True

    def __write_ant_delta_hen(self, ds):
        pass

    def __read_ant_delta_xyz(self, ds, line):
        if not self.ant_delta_xyz:
            self.ant_delta_xyz = Cartesian()
        self.ant_delta_xyz[0] = float(line[0:14])
        self.ant_delta_xyz[1] = float(line[14:28])
        self.ant_delta_xyz[2] = float(line[28:42])
        return True

    def __write_ant_delta_xyz(self, ds):
        pass

    def __read_ant_phase_center(self, ds, line):
        if not self.ant_phase_center:
            self.ant_phase_center = {}
        ss = satellite_system.find_satellite_system(line[0])
        obs_type = ObsType(line[2:5])
        phase_center = Triple()
        phase_center[0] = float(line[5:14])
        phase_center[1] = float(line[14:28])
        phase_center[2] = float(line[28:42])
        self.ant_phase_center[ss] = {obs_type: phase_center}
        return True

    def __write_ant_phase_center(self, ds):
        pass

    def __read_ant_sight_xyz(self, ds, line):
        if not self.ant_sight_xyz:
            self.ant_sight_xyz = Cartesian()
        self.ant_sight_xyz[0] = float(line[0:14])
        self.ant_sight_xyz[1] = float(line[14:28])
        self.ant_sight_xyz[2] = float(line[28:42])
        return True

    def __write_ant_sight_xyz(self, ds):
        pass

    def __read_ant_zerodir_azi(self, ds, line):
        self.ant_zero_dir_azi = float(line[0:14])
        return True

    def __write_ant_zerodir_azi(self, ds):
        pass

    def __read_ant_zerodir_xyz(self, ds, line):
        if not self.ant_zero_dir_xyz:
            self.ant_zero_dir_xyz = Cartesian()
        self.ant_zero_dir_xyz[0] = float(line[0:14])
        self.ant_zero_dir_xyz[1] = float(line[14:28])
        self.ant_zero_dir_xyz[2] = float(line[28:42])
        return True

    def __write_ant_zerodir_xyz(self, ds):
        pass

    def __read_center_of_mass_xyz(self, ds, line):
        if not self.center_of_mass:
            self.center_of_mass = Cartesian()
        self.center_of_mass[0] = float(line[0:14])
        self.center_of_mass[1] = float(line[14:28])
        self.center_of_mass[2] = float(line[28:42])
        return True

    def __write_center_of_mass_xyz(self, ds):
        pass

    def __read_sys_obs_types(self, ds, line):
        if not self.sys_obs_types:
            self.sys_obs_types = {}
        ss = satellite_system.find_satellite_system(line[0])
        ns = int(line[3:6])
        obs_types = []
        index = 6
        while ns > 0:
            if index >= 58:
                line = ds.read_line()
                index = 6
            record = line[index:index+4].strip(' ')
            if len(record) > 0:
                obs_types.append(ObsType(record))
            ns = ns - 1
            index = index + 4
        self.sys_obs_types[ss] = obs_types
        return True

    def __write_sys_obs_types(self, ds):
        pass

    def __read_signal_strength_unit(self, ds, line):
        self.signal_strength_unit = line[0:20]
        return True

    def __write_signal_strength_unit(self):
        pass

    def __read_interval(self, ds, line):
        self.interval = float(line[0:10])
        return True

    def __write_interval(self, ds):
        pass

    def __read_time_of_first_obs(self, ds, line):
        if not self.time_of_first_obs:
            self.time_of_first_obs = CivilTime()
        self.time_of_first_obs.year = int(line[0:6])
        self.time_of_first_obs.month = int(line[6:12])
        self.time_of_first_obs.day = int(line[12:18])
        self.time_of_first_obs.hour = int(line[18:24])
        self.time_of_first_obs.minute = int(line[24:30])
        self.time_of_first_obs.second = float(line[30:43])
        self.time_of_first_obs.time_system = time_system.find_time_system(line[48:51])
        return True

    def __write_time_of_first_obs(self, ds):
        pass

    def __read_time_of_last_obs(self, ds, line):
        if not self.time_of_last_obs:
            self.time_of_last_obs = CivilTime()
        self.time_of_last_obs.year = int(line[0:6])
        self.time_of_last_obs.month = int(line[6:12])
        self.time_of_last_obs.day = int(line[12:18])
        self.time_of_last_obs.hour = int(line[18:24])
        self.time_of_last_obs.minute = int(line[24:30])
        self.time_of_last_obs.second = float(line[30:43])
        self.time_of_last_obs.time_system = time_system.find_time_system(line[48:51])
        return True

    def __write_time_of_last_obs(self, ds):
        pass

    def __read_rcv_clock_offs_applied(self, ds, line):
        self.rcv_clock_offs_applied = int(line[0:6])
        return True

    def __write_rcv_clock_offs_applied(self, ds, line):
        pass

    def __read_sys_dcbs_applied(self, ds, line):
        if not self.sys_dcbs_applied:
            self.sys_dcbs_applied = {}
        ss = satellite_system.find_satellite_system(line[0])
        name = line[2:19]
        source = line[20:60]
        self.sys_dcbs_applied[ss] = {'name': name, 'source': source}
        return True

    def __write_sys_dcbs_applied(self, ds):
        pass

    def __read_sys_pcvs_applied(self, ds, line):
        if not self.sys_pcvs_applied:
            self.sys_pcvs_applied = {}
        ss = satellite_system.find_satellite_system(line[0])
        name = line[2:19]
        source = line[20:60]
        self.sys_pcvs_applied[ss] = {'name': name, 'source': source}
        return True

    def __write_sys_pcvs_applied(self, ds):
        pass

    def __read_sys_scale_factor(self, ds, line):
        if not self.sys_scale_factor:
            self.sys_scale_factor = {}
        ss = satellite_system.find_satellite_system(line[0])
        if ss not in self.sys_scale_factor:
            self.sys_scale_factor[ss] = {}
        factor = int(line[2:6])
        ns = line[8:10].strip(' ')
        if len(ns) == 0 or int(ns) == 0:
            self.sys_scale_factor[ss][factor] = []
            return True
        else:
            ns = int(ns)
        obs_types = []
        index = 10
        while ns > 0:
            if index >= 58:
                line = ds.read_line()
                index = 10
            record = line[index:index+4].strip(' ')
            if len(record) > 0:
                obs_types.append(ObsType(record))
            ns = ns - 1
            index = index + 4
        self.sys_scale_factor[ss][factor] = obs_types
        return True

    def __write_sys_scale_factor(self, ds):
        pass

    def __read_sys_phase_shift(self, ds, line):
        if not self.sys_phase_shift:
            self.sys_phase_shift = {}
        ss = satellite_system.find_satellite_system(line[0])
        if ss not in self.sys_phase_shift:
            self.sys_phase_shift[ss] = {}
        obs_type = ObsType(line[2:5])
        correct = float(line[6:14])
        ns = line[16:18].strip(' ')
        if len(ns) <= 0 or int(ns) == 0:
            self.sys_phase_shift[ss][obs_type] = {'correct': correct, 'sat_ids': []}
            return True
        else:
            ns = int(ns)
        sat_ids = []
        index = 18
        while ns > 0:
            if index >= 58:
                line = ds.read_line()
                index = 18
            record = line[index:index+4].strip(' ')
            if len(record) > 0:
                sat_ids.append(SatID().parse(record))
            ns = ns - 1
            index = index + 4
        self.sys_phase_shift[ss][obs_type] = {'correct': correct, 'sat_ids': sat_ids}
        return True

    def __write_sys_phase_shift(self, ds):
        pass

    def __read_glo_slot_and_frq(self, ds, line):
        if not self.glo_slot_and_frq:
            self.glo_slot_and_frq = {}
        ns = int(line[0:3])
        index = 4
        while ns > 0:
            if index >= 56:
                line = ds.read_line()
                index = 4
            record = line[index:index+4].strip(' ')
            if len(record) > 0:
                sat_id = SatID().parse(record)
                frq = int(line[index+4:index+7].strip(' '))
                self.glo_slot_and_frq[sat_id] = frq
            ns = ns - 1
            index = index + 7
        return True

    def __write_glo_slot_and_frq(self):
        pass

    def __read_glo_cod_phs_bis(self, ds, line):
        if not self.glo_cod_phs_bis:
            self.glo_cod_phs_bis = {}
        ns = 4
        index = 0
        while ns > 0:
            obs_type = ObsType(line[index:index+4].strip(' '))
            bis = float(line[index+4:index+12].strip(' '))
            index += 13
            ns -= 1
            self.glo_cod_phs_bis[obs_type] = bis
        return True

    def __write_glo_cod_phs_bis(self, ds):
        pass

    def __read_number_of_satellite(self, ds, line):
        self.number_of_satellite = int(line[0:6])
        return True

    def __write_number_of_satellite(self, ds, line):
        pass


class RNXObsV3Epoch(object):

    def __init__(self, sys_obs_types):
        self.epoch = CivilTime(time_system.UTC)
        self.flag = 0
        self.ns = 0
        self.rcv_clock_offset = 0.0
        self.sys_obs_types = sys_obs_types
        self.obs_map = None
        self.event_list = None

    def read(self, ds):
        line = ds.read_line().strip(' ').strip()
        if not line:
            return False
        if not self.__read_first_line(line):
            raise Exception('Observation record have error format.')
        if self.flag in [0, 1, 6]:
            return self.__read_obs_record(ds)
        else:
            return self.__read_event_record(ds)

    def __read_first_line(self, line):
        if line[0] != '>':
            return False
        self.flag = int(line[31:32])
        self.ns = int(line[32:35])
        if self.flag not in [3, 4]:
            self.epoch.year = int(line[2:6])
            self.epoch.month = int(line[7:9])
            self.epoch.day = int(line[10:12])
            self.epoch.hour = int(line[13:15])
            self.epoch.minute = int(line[16:18])
            self.epoch.second = float(line[18:29])
        if len(line) >= 56:
            self.rcv_clock_offset = float(line[41:56])
        return True

    def __read_obs_record(self, ds):
        if not self.obs_map:
            self.obs_map = {}
        num = self.ns
        while num > 0:
            record = ds.read_line().strip()
            i = 3
            sat_id = SatID().parse(record[0:3])
            if sat_id not in self.obs_map:
                self.obs_map[sat_id] = {}
            obs_types = self.sys_obs_types[sat_id.satellite_system]
            max_len = len(record)
            for obs_type in obs_types:
                value = record[i:i+14].strip(' ')
                if len(value) > 0 and '0.0' != value:
                    value = float(value)
                    if i+14 >= max_len or record[i+14].strip(' ') == '':
                        lli = 0
                    else:
                        lli = int(record[i+14])
                    if i+15 >= max_len or record[i+15].strip(' ') == '':
                        sn = 0
                    else:
                        sn = int(record[i+15])
                    self.obs_map[sat_id][obs_type] = [value, lli, sn]
                i += 16
            num -= 1
        return True

    def __read_event_record(self, ds):
        if not self.event_list:
            self.event_list = []
        num = self.ns
        while num > 0:
            self.event_list.append(ds.read_line().strip())
            num -= 1
        return True

    def is_valid(self):
        return self.flag in [0, 1]



