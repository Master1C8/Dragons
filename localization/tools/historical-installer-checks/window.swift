import AppKit
import CoreGraphics
let target = pid_t(CommandLine.arguments[1])!
let front = NSWorkspace.shared.frontmostApplication?.processIdentifier == target
let windows = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID) as? [[String: Any]] ?? []
let visible = windows.filter { ($0[kCGWindowOwnerPID as String] as? pid_t) == target }.count
print("\(front ? 1 : 0) \(visible)")
