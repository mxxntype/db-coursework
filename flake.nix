{
    description = "mxxntype's MIREA Database coursework";

    inputs = {
        # SECTION: Core inputs.
        nixpkgs.url = "github:nixos/nixpkgs/nixos-23.11";

        # SECTION: Nix libraries.
        # Nix flake framework.
        snowfall-lib = {
            url = "github:snowfallorg/lib";
            inputs.nixpkgs.follows = "nixpkgs";
        };
    };

    outputs = inputs: inputs.snowfall-lib.mkFlake {
        inherit inputs;
        src = ./.;

        # Snowfall Lib configuration.
        snowfall.namespace = "db-coursework";
    };
}
