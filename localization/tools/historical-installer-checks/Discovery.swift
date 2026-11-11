import Foundation

@main struct Discovery {
    static func main() throws {
        let config = try PackageConfig.load(from: URL(fileURLWithPath: CommandLine.arguments[1]))
        let core = InstallerCore()
        let home = FileManager.default.homeDirectoryForCurrentUser
        let stock = home.appendingPathComponent("Documents/Drag'N Wash.app")
        let actual = core.detectInstallation(config: config, searchRoots: [home])
        guard actual?.appBundle.path == stock.path else { fatalError("Unexpected target: \(String(describing: actual?.appBundle.path))") }
        let fixture = URL(fileURLWithPath: CommandLine.arguments[2])
        let nested = fixture.appendingPathComponent("one/two/Renamed.app")
        let result = core.detectInstallation(config: config, searchRoots: [fixture])
        precondition(result?.appBundle.path == nested.path)
        let executable = nested.appendingPathComponent("Contents/MacOS/DragNWash")
        precondition(core.resolveInstallation(executable, appID: config.steamAppID)?.appBundle.path == nested.path)
        print("Found actual standalone app and renamed nested fixture. Explicit executable resolved.")
    }
}
