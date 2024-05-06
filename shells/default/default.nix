{
    pkgs,
    ...
}:

pkgs.mkShell {
    NIX_CONFIG = "extra-experimental-features = nix-command flakes repl-flake";

    nativeBuildInputs = with pkgs; [
        pkg-config
    ];

    buildInputs = with pkgs; [
        postgresql
        ruff-lsp
        (python311.withPackages (ps: with ps; [
            psycopg2
            pyqt6
            qdarkstyle
            python-lsp-server
            colorlog
        ]))
    ];
}
