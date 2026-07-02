// Lunr's default trimmer treats non-Latin text as punctuation.
// Replace it once with a Unicode-aware trimmer so Korean terms remain indexed.
if (!this.__unicodeTrimmerConfigured) {
  var unicodeTrimmer = function (token) {
    return token.update(function (text) {
      return text
        .replace(/^[^\p{L}\p{N}]+/u, "")
        .replace(/[^\p{L}\p{N}]+$/u, "");
    });
  };

  lunr.Pipeline.registerFunction(unicodeTrimmer, "unicodeTrimmer");
  this.pipeline.remove(lunr.trimmer);
  this.pipeline.before(lunr.stopWordFilter, unicodeTrimmer);
  this.__unicodeTrimmerConfigured = true;
}
