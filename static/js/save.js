$(function () {
  function reloadMarkdown() {
    $('#slides-frame')[0].contentWindow.postMessage(JSON.stringify({
      method: 'reloadMarkdown'
    }), window.location.origin);
  }

  window.save = function () {
    var editor = ace.edit("editor");

    $.post("/save/"+window.filename, {
      content: editor.getValue(),
    }, reloadMarkdown);
  };

  $('#editor').keyup($.debounce(window.save, 600));
});
