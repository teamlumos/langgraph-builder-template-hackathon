{pkgs}: {
  deps = [
    pkgs.playwright-driver
    pkgs.gitFull
    pkgs.glibcLocales
    pkgs.playwright
    pkgs.bash
    pkgs.unzip
  ];
  env = {
    PLAYWRIGHT_BROWSERS_PATH = "${pkgs.playwright-driver.browsers}";
    PLAYWRIGHT_SKIP_VALIDATE_HOST_REQUIREMENTS = true;
  };
}
