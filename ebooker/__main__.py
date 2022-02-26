from ebooker.main import parse_cli_config, main

epub_file = main(config=parse_cli_config())
print(f"Finished! Saved to {epub_file=}")
