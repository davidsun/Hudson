$.posts = {
  bindLikeLink: function(element){
    var t = $(element);
    var post_id = t.attr("post-id");
    var liked = (t.attr("liked") == "true");
    if (liked){
      t.html("已收藏").unbind("hover").hover(function(){
        t.html("取消收藏");
      }, function(){
        t.html("已收藏");
      });
      t.unbind("click").click(function(){
        $.get("/posts/" + post_id + "/unlike");
        t.attr("liked", "false");
        $.posts.bindLikeLink(t);
      });
    } else {
      t.html("收藏").unbind("hover");
      t.unbind("click").click(function(){
        $.get("/posts/" + post_id + "/like");
        t.attr("liked", "true");
        $.posts.bindLikeLink(t);
      });
    }
  },

  showInList: function(element){
    var t = $(element);
    t.find("a[data-toggle='like-link']").each(function(){
      $.posts.bindLikeLink(this);
    });
    t.find(".post-bottom a").addClass("muted");
    t.unbind('hover').hover(function(){
      t.find(".post-bottom a").removeClass("muted");
    }, function(){
      t.find(".post-bottom a").addClass("muted");
    });
  },

  showSingle: function(element){
    var t = $(element);
    t.find("a[data-toggle='like-link']").each(function(){
      $.posts.bindLikeLink(this);
    });
  }
};

$.fn.showListPost = function(){
  $.posts.showInList(this);
};

$.fn.showSinglePost = function(){
  $.posts.showSingle(this);
}