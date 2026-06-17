# （OPT）WSL上需要打通摄像头

## 检查 WSL 能否通过 usbipd 获取摄像头

### Windows 侧（管理员 PowerShell）

```powershell
usbipd list
```
查看是否有摄像头设备（通常显示 "USB Video Device"）。

若没有先安装 usbipd：`winget install usbipd`

### usbipd 分享与挂载流程

**Windows 侧（管理员 PowerShell）—— 绑定并分享设备**

```powershell
# 列出所有 USB 设备，找到摄像头的 BUSID（例如 3-2）
usbipd list

# 绑定分享该设备
usbipd bind --busid 3-2
```

绑定后 `usbipd list` 该设备状态会变为 `Shared`。

**WSL 侧 —— 挂载到 WSL**
```bash
# 先查 Windows 主机的 IP
ip route show | grep default | awk '{print $3}'

# 将绑定的 USB 设备挂载到 WSL
sudo usbip attach -r <Windows-IP> -b 3-2
```
此时 `lsusb` 应能看到该摄像头设备，进入下一步验证。

> **注意**: 如果 WSL 之前 attach 过但设备断开导致 `usbip: error: already connected to a virtual host bus`，先 `usbip port` 查看端口号，再用 `sudo usbip detach -p <端口号>` 断开重连。

### WSL 侧

**1. 安装基础工具**

```bash
sudo apt update && sudo apt install usbutils linux-tools-generic linux-tools-$(uname -r)
```

**2. 加载内核模块**
```bash
# USB/IP 模块
sudo modprobe vhci-hcd
sudo modprobe usbip-core
sudo modprobe usbip-host

# UVC 摄像头模块
sudo modprobe uvcvideo
```

**3. 确认设备可见**
```bash
lsusb                    # 应看到挂载后的摄像头
ls /dev/video*           # 应看到 /dev/video0 等
```

**4. 验证 UVC 驱动状态**
```bash
# 确认模块已加载
lsmod | grep uvcvideo

# 检查内核是否编译了 UVC 支持
zgrep CONFIG_USB_VIDEO_CLASS /proc/config.gz 2>/dev/null || cat /boot/config-$(uname -r) 2>/dev/null | grep CONFIG_USB_VIDEO_CLASS
```

在新的WSL内核中都已经有了uvcvideo模块，所以一般不需要担心内核编译问题。最多只是可能没有加载而已。

### 完整一键检测脚本
```bash
echo "=== USB/IP Modules ==="
sudo modprobe vhci-hcd && echo "vhci-hcd OK" || echo "vhci-hcd FAIL"
sudo modprobe usbip-core && echo "usbip-core OK" || echo "usbip-core FAIL"

echo "=== UVC Driver ==="
sudo modprobe uvcvideo && echo "uvcvideo OK" || echo "uvcvideo FAIL"
ls /dev/video* 2>/dev/null && echo "video devices found" || echo "no /dev/video*"

echo "=== lsusb ==="
lsusb || echo "lsusb not found, install usbutils"

echo "=== USB/IP status ==="
lsmod | grep usbip

echo "=== WSL kernel version ==="
uname -r
```

## 其他方法

直接使用webcam方案，把摄像头共享给Windows系统，WSL通过网络访问Windows上的摄像头数据流（如使用IP Webcam等工具）。但这种方案可能存在性能和延迟问题，不推荐用于实时性要求较高的应用。但是作为开发来说肯定是够了。

而且在开发阶段，我的建议是直接使用录制的demo视频，连usbipd通进来的摄像头都用不上。
