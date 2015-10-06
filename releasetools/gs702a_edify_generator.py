# Copyright (C) 2009 The Android Open Source Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os, sys

LOCAL_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RELEASETOOLS_DIR = os.path.abspath(os.path.join(LOCAL_DIR, '../../../build/tools/releasetools'))

import edify_generator

class EdifyGenerator(edify_generator.EdifyGenerator):
    def FlashBoot(self, image, partition):
	  """Flash a gs702a misc and boot section."""

      args = {'image': image, 'partition': partition}

      self.script.append(
	        ('mount("vfat", "EMMC", "%(partition)s", "/misc");\n'
             '       package_extract_dir("system/kernel/misc", "/misc");\n'
             '       package_extract_file("%(image)s", "/misc/%(image)s");\n'
             '       unmount("/misc");') % args)

    def Unmount(self, mount_point):
      """Unmount the partition with the given mount_point."""
      fstab = self.info.get("fstab", None)
      if fstab:
        p = fstab[mount_point]
        self.script.append('unmount("%s");' %
								(p.mount_point))
        self.mounts.add(p.mount_point)