import Foundation

@main
struct TestInstaller {
    static func main() throws {
        let root = URL(fileURLWithPath: CommandLine.arguments[1])
        let payload = URL(fileURLWithPath: CommandLine.arguments[2])
        let config = try PackageConfig.load(from: payload.appendingPathComponent("PackageConfig.json"))
        let core = InstallerCore()
        for lang in ["ar", "ja", "es-419", "pt-BR", "zh-TW", "ar"] {
            guard let game = core.resolveInstallation(root, appID: config.steamAppID) else {
                throw InstallerError.invalidGameFolder
            }
            try core.install(payload: payload.appendingPathComponent("LocalizationPayload"),
                             config: config, selectedRuntimeCode: lang, into: game)
            let info = config.languages.first { $0.runtimeCode == lang }!
            for file in config.payloadFiles(for: info) {
                let actual = try InstallerCore.sha256(of: game.dataDirectory.appendingPathComponent(file.path))
                guard actual == file.payloadSHA256 else { throw InstallerError.payloadChecksumMismatch(file.path) }
            }
            let receipt = game.appBundle.appendingPathComponent("Contents/Resources/VNRevival/dragons-vnrevival/receipt.json")
            let json = try JSONSerialization.jsonObject(with: Data(contentsOf: receipt)) as? [String: Any]
            guard (json?["activeLanguage"] as? [String: String])?["siteLocale"] == lang else {
                throw InstallerError.malformedReceipt
            }
            print("verified install and persisted locale: \(lang)")
        }
    }
}
