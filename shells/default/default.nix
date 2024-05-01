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
        libpqxx
        glade
        gtkmm4.dev
        glibmm.dev
        glib

        (python311.withPackages (ps: with ps; [
            psycopg2
            pyqt6
        ]))
    ];
}
