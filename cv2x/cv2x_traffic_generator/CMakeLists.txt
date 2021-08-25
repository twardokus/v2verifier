#
# Copyright 2013-2020 Software Radio Systems Limited
#
# This file is part of srsLTE
#
# srsLTE is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of
# the License, or (at your option) any later version.
#
# srsLTE is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# A copy of the GNU Affero General Public License can be found in
# the LICENSE file in the top-level directory of this distribution
# and at http://www.gnu.org/licenses/.
#

add_executable(cv2x_traffic_generator cv2x_traffic_generator.c)
target_link_libraries(cv2x_traffic_generator srslte_phy srslte_common srslte_rf pthread)

install(TARGETS cv2x_traffic_generator DESTINATION ${RUNTIME_DIR})

########################################################################
# Install library headers
########################################################################
INSTALL(  DIRECTORY include/
        DESTINATION "${INCLUDE_DIR}"
        FILES_MATCHING PATTERN "*.h" )
