# COSMIC Rices

A gallery of every cosmic-*-theme rice for the COSMIC desktop on Pop!_OS: 14 themes, each with a dark and a light half.

**[Open the gallery](https://atraxsrc.github.io/cosmic-rices/)**

Each card shows a rice in its own colours, with its screenshot, palette and links to install it. Flip one card between its Night and Day halves, or switch every card at once. Click a swatch to copy its colour.

## Install a rice

```bash
curl -fsSL https://raw.githubusercontent.com/atraxsrc/themebox/master/install.sh | bash
themebox get noir
themebox switch noir
```

[themebox](https://github.com/atraxsrc/themebox) also adds a panel button that flips between a rice's dark
and light halves. To install a rice by hand, follow the Setup section in its README.

## How it is built

Nothing on the page is typed in by hand. `build.py` reads the sibling `cosmic-*-theme` repositories (the name, tagline and pairing from each README, the palette table, the Firefox add-on link, and the dark or light mode from `scripts/switch.sh`), makes 960 px JPEG thumbnails of each screenshot with ImageMagick, and writes `index.html`.

```sh
python3 build.py          # rebuild after changing a rice
python3 build.py --data   # print what it extracted
```

It expects the theme repositories cloned next to this one. Needs Python 3 and ImageMagick (`convert`).

## License

MIT. Screenshots and palettes belong to their rices; see each repository for credits.
