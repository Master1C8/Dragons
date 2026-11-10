// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "DragonsInstaller",
    platforms: [.macOS(.v14)],
    products: [
        .executable(
            name: "DragonsInstaller",
            targets: ["DragonsInstaller"]
        ),
    ],
    targets: [
        .executableTarget(
            name: "DragonsInstaller",
            resources: [
                .copy("Resources/PackageConfig.json"),
                .copy("Resources/LocalizationPayload"),
            ]
        ),
    ]
)
