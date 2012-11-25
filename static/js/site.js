$.site = {
  showModal: function(url, options){
    var t = $(".hudson-modal");
    options = options || {};
    if (options.title) t.find(".modal-header h3").html(options.title);
    t.find(".modal-body").html("正在载入，请稍后...");
    t.modal();
    $.get(url, function(data){
      t.find(".modal-body").html(data);
    });
  }
};

$(document).ready(function(){
  $("[data-toggle='hudson-modal']").unbind("click").click(function(){
    var options = {};
    options.title = $(this).attr("title");
    $.site.showModal($(this).attr("url"), options);
  });
});