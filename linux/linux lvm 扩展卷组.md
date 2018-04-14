# linux lvm 扩展卷组

一般虚拟机硬盘快满 或想要扩充linux 系统盘大小时 使用 
```
df -lh  列出个分区使用情况 
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/vg_centos6-lv_root
                       18G   15G  2.0G  89% /
tmpfs                 931M     0  931M   0% /dev/shm
/dev/sda1             477M   28M  425M   7% /boot

fdisk -l 列出磁盘列表
[root@centos6 home]# fdisk -l

Disk /dev/loop0: 20.8 GB, 20842571264 bytes
255 heads, 63 sectors/track, 2533 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/loop1: 20.4 GB, 20424163328 bytes
255 heads, 63 sectors/track, 2483 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x8b9ae303


Disk /dev/sda: 1099.5 GB, 1099511627776 bytes
255 heads, 63 sectors/track, 133674 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x000b14cb

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *           1          64      512000   83  Linux
Partition 1 does not end on cylinder boundary.
/dev/sda2              64        2611    20458496   8e  Linux LVM

Disk /dev/mapper/vg_centos6-lv_root: 18.8 GB, 18798870528 bytes
255 heads, 63 sectors/track, 2285 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000


Disk /dev/mapper/vg_centos6-lv_swap: 2147 MB, 2147483648 bytes
255 heads, 63 sectors/track, 261 cylinders
Units = cylinders of 16065 * 512 = 8225280 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000

```
如上所示 
/dev/mapper/vg_centos6-lv_root 想扩展此lv 
可使用如下命令
```
首先创建一个分区
fdisk /dev/sda
输入n
一路回车
记得修改类型为lvm 输入命令t 类型为8e
最后w保存

执行 partprobe /dev/sda 使其生效 不用重启
如果提示partrobe command not found 
则执行yum install parted -y
执行后 
cat /proc/partitions 查看是否可以看到 新建分区sda3
[root@centos6 home]# cat /proc/partitions
major minor  #blocks  name

   7        0   20354073 loop0
   7        1   19945472 loop1
   8        0 1073741824 sda
   8        1     512000 sda1
   8        2   20458496 sda2
 253        0   18358272 dm-0
 253        1    2097152 dm-1


```
接着创建 物理卷

```
[root@centos6 ~]# pvcreate /dev/sda3
  Physical volume "/dev/sda3" successfully created

[root@centos6 ~]# pvs #查看当前物理卷有哪些
  PV         VG         Fmt  Attr PSize    PFree
  /dev/sda2  vg_centos6 lvm2 a--u   19.51g       0
  /dev/sda3             lvm2 ---- 1003.99g 1003.99g


```
扩展卷组

```
[root@centos6 ~]# vgextend vg_centos6 /dev/sda3
  Volume group "vg_centos6" successfully extended
[root@centos6 ~]# vgs
  VG         #PV #LV #SN Attr   VSize    VFree
  vg_centos6   2   2   0 wz--n- 1023.50g 1003.99g
[root@centos6 ~]# lvs
  LV      VG         Attr       LSize  Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  lv_root vg_centos6 -wi-ao---- 17.51g
  lv_swap vg_centos6 -wi-ao----  2.00g
[root@centos6 ~]# lvdisplay
  --- Logical volume ---
  LV Path                /dev/vg_centos6/lv_root
  LV Name                lv_root
  VG Name                vg_centos6
  LV UUID                USkB26-pXrs-bwvz-frOZ-SmVG-k7sc-iTrYRp
  LV Write Access        read/write
  LV Creation host, time centos6.9, 2017-06-08 17:49:29 -0400
  LV Status              available
  # open                 1
  LV Size                17.51 GiB
  Current LE             4482
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:0

  --- Logical volume ---
  LV Path                /dev/vg_centos6/lv_swap
  LV Name                lv_swap
  VG Name                vg_centos6
  LV UUID                6DnHKM-AwA1-lkin-8RxB-P4xq-txvB-uIT1Hf
  LV Write Access        read/write
  LV Creation host, time centos6.9, 2017-06-08 17:49:33 -0400
  LV Status              available
  # open                 1
  LV Size                2.00 GiB
  Current LE             512
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:1



```
最后扩展系统使用卷 并使用resize2fs /dev/mapper/vg_centos6-lv_root 使其生效
```
[root@centos6 ~]# lvextend -L +1000G /dev/vg_centos6/lv_root
  Size of logical volume vg_centos6/lv_root changed from 17.51 GiB (4482 extents) to 1017.51 GiB (260482 extents).
  Logical volume lv_root successfully resized.

[root@centos6 ~]# resize2fs /dev/mapper/vg_centos6-lv_root
resize2fs 1.41.12 (17-May-2010)
Filesystem at /dev/mapper/vg_centos6-lv_root is mounted on /; on-line resizing required
old desc_blocks = 2, new_desc_blocks = 64
Performing an on-line resize of /dev/mapper/vg_centos6-lv_root to 266733568 (4k) blocks.
The filesystem on /dev/mapper/vg_centos6-lv_root is now 266733568 blocks long.

[root@centos6 public]# df -lh
Filesystem            Size  Used Avail Use% Mounted on
/dev/mapper/vg_centos6-lv_root
                     1002G   46G  906G   5% /
tmpfs                 931M     0  931M   0% /dev/shm
/dev/sda1             477M   28M  425M   7% /boot


```
如上所示 / 已扩展为1002G
