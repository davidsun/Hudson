$.posts = {
  bindCommentLink: function(comments_block, element){
    var t = $(element);
    var post_id = t.attr("post-id");
    comments_block = $(comments_block);
    comments_block.hide();
    t.attr("shown", "false");
    t.unbind("click").click(function(){
      if (t.attr("shown") == "true"){
        comments_block.hide();
        t.attr("shown", "false");
        var count = comments_block.find(".posts-comments-list .comment").length;
        if (count === null) count = 0;
        t.html("回复(" + count + ")");
      } else {
        comments_block.show();
        t.attr("shown", "true");
        t.html("收起回复");
        $.get("/posts/" + post_id + "/comments", function(result){
          comments_block.find(".comments-list").html(result);
        });
      }
    });
  },

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
          }
        });
      });
    }
  },

  initPostComment: function(element){
    var t = $(element);
    var post_id = t.attr("post-id");
    
    t.find(".post").atTips();
    t.submit(function(){
      var content = $(this).find(".post").val();
      var error = "";
      if (content.length === 0) error = "请输入您希望发布的内容...";
      else if (content.length > 200) error = "您输入的内容太长了。";
      if (error.length > 0){
        $(this).find(".post").tooltip({
          placement: 'top',
          title: error,
          trigger: "manual"
        }).tooltip("show");
        $(this).find(".post").unbind('click keydown').bind('click keydown', function(){
          $(this).tooltip('destroy');
        });
        return false;
      }
      $(this).find(".btn-primary").addClass("disabled").html("正在发布，请稍后...");
      $.post("/posts/" + post_id + "/comments", {
        "content": content,
        "csrfmiddlewaretoken": $(this).find("input[name='csrfmiddlewaretoken']").val()
      }, function(result){
        if (result.status == "ok"){
          $.get("/posts/" + post_id + "/comments", function(result){
            t.parent().find(".comments-list").html(result);
          });
          t.find(".btn-primary").removeClass("disabled").html("发布评论");
          t.find(".post").val("");
        }
      });
      return false;
    });
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

    if (post_count === 0){
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
    t.find(".form-post").each(function(){
      $.posts.initPostComment(this);
    });
    t.find("a[data-toggle='comments-link']").each(function(){
      $.posts.bindCommentLink(t.find(".comments"), this);
    });
  },

  showSingle: function(element){
    var t = $(element);
    t.find("a[data-toggle='like-link']").each(function(){
      $.posts.bindLikeLink(this);
    });
    t.find(".form-post").each(function(){
      $.posts.initPostComment(this);
    });
  }
};

$.fn.initPostAppendingList = function(options){
  $.posts.initAppendingList(this, options);
};

$.fn.showListPost = function(){
  $.posts.showInList(this);
};

$.fn.showSinglePost = function(){
  $.posts.showSingle(this);
};

