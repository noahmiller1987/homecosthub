/** Tailwind v3 config. Every class lives as a literal string in generate.py, so that is the
 *  only file scanned (seconds, not 2,000 HTML files). Rebuild: ./build_css.sh */
module.exports = {
  content: ["./generate.py"],
  theme: { extend: {} },
  plugins: [],
};
