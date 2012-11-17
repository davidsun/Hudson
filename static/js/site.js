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
        $.get("/posts/" + post_id + "/unlike", function(result){
          if (result.status == "ok"){
            t.attr("liked", "false");
            $.posts.bindLikeLink(t);
          } else {
            $(this).find(".post").tooltip({
              placement: 'top',
              title: "取消收藏失败", 
              trigger: "manual",
            }).tooltip("show");
          }
        });
      });
    } else {
      t.html("收藏").unbind("hover");
      t.unbind("click").click(function(){
        $.get("/posts/" + post_id + "/like", function(result){
          if (result.status == "ok"){
            t.attr("liked", "true");
            $.posts.bindLikeLink(t); 
          } else {
            $(this).find(".post").tooltip({
              placement: 'top',
              title: "收藏失败", 
              trigger: "manual",
            }).tooltip("show");
          }
        });
      });
    }
  },

  initAppendingList: function(element, options){
    var t = $(element);
    var btn = t.find(".list-indicator a");
    var post_count = t.find(".posts-list-post").length;
    var url_params = $.url().param();
    var url_path = $.url().attr('path');
    var is_loading = false;

    function loadPosts(){
      if (is_loading) return;
      is_loading = true;
      btn.html("正在载入，请稍后...").unbind("click");
      url_params['offset'] = post_count;
      $.get(url_path, url_params, function(result){
        t.find(".posts-appending-list-posts").append(result);
        var new_post_count = t.find(".posts-list-post").length;
        if (new_post_count > post_count){
          $.posts.initAppendingList(t, options);
        } else {
          btn.html("没有更多新鲜事了...");
          btn.addClass("disabled");
        }
      });
    }

    if (post_count == 0){
      btn.html("没有更多新鲜事了...");
      btn.addClass("disabled");
    }  else {
      if (options && options.auto_load){
        if ($(window).scrollTop() > $(document).height() - $(window).height() - $(window).height() / 2) loadPosts();
        $(window).scroll(function(){
          if ($(window).scrollTop() > $(document).height() - $(window).height() - $(window).height() / 2){
            loadPosts();
          }
        });
      }

      btn.removeClass("disabled").html("更多新鲜事...").unbind("click").click(function(){
        loadPosts();
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
  },
};

$.fn.initPostAppendingList = function(options){
  $.posts.initAppendingList(this, options);
};

$.fn.showListPost = function(){
  $.posts.showInList(this);
};

$.fn.showSinglePost = function(){
  $.posts.showSingle(this);
}

