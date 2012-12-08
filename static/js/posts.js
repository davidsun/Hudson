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
        var count = comments_block.find(".comments-list .comment").length;
        if (count === null) count = 0;
        t.html("回复(" + count + ")");
      } else {
        comments_block.show();
        t.attr("shown", "true");
        t.html("收起回复");
        $.get("/posts/" + post_id + "/comments", function(result){
          var ar = {
            "comments" : ko.observableArray(result)
          };
          ko.applyBindings(ar, comments_block[0]);
        });
      }
    });
  },

  bindTagLink: function(tags_block, add_tag_block, element){
    var t = $(element);
    var post_id = t.attr("post-id");
    var content = t.html();
    var content = content.replace(/(^\s*)|(\s*$)/g, "");
    var callbackFunc = function(result){
      if (result.status == "ok"){
        $.get("/posts/" + post_id + "/tags", function(result){
          if (result.user_tag == null) {
            result.user_tag = "加标签";
            add_tag_block.find(".untag").hide();
          } else {
            result.user_tag =  "标签:"+result.user_tag;
            add_tag_block.find(".untag").show();
          }
          for (var i = 0; i < result.tags.length; i ++)
            result.tags[i].content += '(' + result.tags[i].count + ')';
          result.tags = ko.observableArray(result.tags);
          tags_block.html("");
          ko.applyBindings(result, tags_block[0]);
          ko.applyBindings(result, add_tag_block[0]);
        });
      }
    };
    t.unbind("click").click(function(){
      if (content == "删除标签"){
        $.post("/posts/" + post_id + "/untag", { 
          "csrfmiddlewaretoken": add_tag_block.find("input[name='csrfmiddlewaretoken']").val()
        },callbackFunc);
      } else {
        $.post("/posts/" + post_id + "/tags", {
          "content": content,
          "csrfmiddlewaretoken": add_tag_block.find("input[name='csrfmiddlewaretoken']").val()
        },callbackFunc);  
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

  bindRepostLink: function(post_block, element){
    var t = $(element);
    var post_id = t.attr("post-id");

    post_block = $(post_block);
    t.click(function(){
      if (post_block.find(".original").length > 0){
        $(".modal-repost-post .original-post").html("<b>" + post_block.find(".original-username").html() + ": </b>" +
          post_block.find(".original-content").html());
        $(".modal-repost-post .content").val("//@" + $.trim(post_block.find(".username").html()) + " " + post_block.find(".content").text());
      } else {
        $(".modal-repost-post .original-post").html("<b>" + post_block.find(".username").html() + ": </b>" +
          post_block.find(".content").html());
        $(".modal-repost-post .content").val("//@" + $.trim(post_block.find(".username").html()));
      }
      $(".modal-repost-post button[type='submit']").addClass("b.atTips()tn-primary").removeClass("btn-success").html("发送");
      $(".modal-repost-post").on("shown", function(){
        $(this).find(".content").focus().atTips();
      });
      $(".modal-repost-post").modal('show');
      $(".modal-repost-post").unbind("submit").submit(function(){
        var t = $(this);
        var content = t.find(".content").val();
        var error = "";

        if (content.length === 0) error = "请输入您希望发布的内容...";
        else if (content.length > 200) error = "您输入的内容太长了。";
        if (error.length > 0){
          t.find(".content").tooltip({
            placement: 'top',
            title: error,
            trigger: "manual"
          }).tooltip("show").data('tooltip').tip().css('z-index', 2080);
          t.find(".content").unbind('click keydown').bind('click keydown', function(){
            $(this).tooltip('destroy');
          });
          return false;
        }
        t.unbind("click").find("button[type='submit']").addClass("disabled").html("正在发送，请稍后...");
        $.post("/posts", {
          "content": content,
          "original_id": post_id,
          "csrfmiddlewaretoken": $(this).find("input[name='csrfmiddlewaretoken']").val()
        }, function(result){
          if (result.status == "ok"){
            t.find("button[type='submit']").removeClass("disabled").removeClass("btn-primary").addClass("btn-success").html("发送成功！");
            setTimeout(function(){
              window.location.reload();
            }, 1500);
          }
        });
        return false;
      });
    });
  },

  initPostComment: function(comments_block, element){
    var t = $(element);
    var post_id = t.attr("post-id");
    
    comments_block = $(comments_block);
    t.find(".reply").atTips();
    t.submit(function(){
      var content = $(this).find(".reply").val();
      var error = "";
      if (content.length === 0) error = "请输入您希望发布的内容...";
      else if (content.length > 200) error = "您输入的内容太长了。";
      if (error.length > 0){
        $(this).find(".reply").tooltip({
          placement: 'top',
          title: error,
          trigger: "manual"
        }).tooltip("show");
        $(this).find(".reply").unbind('click keydown').bind('click keydown', function(){
          $(this).tooltip('destroy');
        });
        return false;
      }
      $(this).find(".btn-primary").addClass("disabled").html("正在发布，请稍候...");
      $.post("/posts/" + post_id + "/comments", {
        "content": content,
        "csrfmiddlewaretoken": $(this).find("input[name='csrfmiddlewaretoken']").val()
      }, function(result){
        if (result.status == "ok"){
          $.get("/posts/" + post_id + "/comments", function(result){
            comments_block.find(".comments-list").html("");
            var ar = {"comments": ko.observableArray(result)};
            ko.applyBindings(ar, comments_block.find(".comments-list")[0]);
          });
          t.find(".btn-primary").removeClass("disabled").html("评论");
          t.find(".reply").val("");
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
    t.find("a[data-toggle='repost-link']").each(function(){
      $.posts.bindRepostLink(t, this);
    });
    t.find(".post-bottom a").addClass("muted");
    t.unbind('hover').hover(function(){
      t.find(".post-bottom a").removeClass("muted");
    }, function(){
      t.find(".post-bottom a").addClass("muted");
    });
    t.find(".form-reply").each(function(){
      $.posts.initPostComment(t.find(".comments"), this);
    });
    t.find("a[data-toggle='comments-link']").each(function(){
      $.posts.bindCommentLink(t.find(".comments"), this);
    });
    t.find("a[data-toggle='tag-link']").each(function(){
      $.posts.bindTagLink(t.find(".post-tags"),t.find(".add-tag"),this)
    });
  },

  showSingle: function(element){
    var t = $(element);
    t.find("a[data-toggle='like-link']").each(function(){
      $.posts.bindLikeLink(this);
    });
    t.find("a[data-toggle='repost-link']").each(function(){
      $.posts.bindRepostLink(t, this);
    });
    t.find(".form-reply").each(function(){
      $.posts.initPostComment(t.find(".comments"), this);
    });
    t.find("a[data-toggle='tag-link']").each(function(){
      $.posts.bindTagLink(t.find(".post-tags"),t.find(".add-tag"),this)
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

