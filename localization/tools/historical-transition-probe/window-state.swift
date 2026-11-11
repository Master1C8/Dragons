import AppKit
import CoreGraphics

let target = pid_t(CommandLine.arguments[1])!
guard let app = NSRunningApplication(processIdentifier: target) else {
    print("Game process not found"); exit(1)
}
let shown = CGWindowListCopyWindowInfo([.optionOnScreenOnly, .excludeDesktopElements], kCGNullWindowID)
    as? [[String: Any]] ?? []
let gameWindows = shown.filter {
    ($0[kCGWindowOwnerPID as String] as? pid_t) == target
}
let foreground = NSWorkspace.shared.frontmostApplication?.processIdentifier
print("gamePID=\(target) hidden=\(app.isHidden) active=\(app.isActive) ownsForeground=\(foreground == target) onScreenWindowCount=\(gameWindows.count)")
