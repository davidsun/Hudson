$.users = {
  showFollowButton: function(element){
    var t = $(element);
    var user_id = t.attr("user-id");
    if (t.attr("followed") == "true"){
      t.removeClass("btn-danger").removeClass("btn-primary").html("已关注");
      t.unbind('hover').hover(function(){
        t.addClass("btn-danger").html("取消关注");
      }, function(){
        t.removeClass("btn-danger").html("已关注");
      });
    } else {
      t.removeClass("btn-danger").addClass("btn-primary").html("关注");
      t.unbind("hover");
    }
    t.unbind('click').click(function(){
      if (t.attr("followed") == "true"){
        $.get("/users/" + user_id + "/unfollow");
        t.attr("followed", "false");
      } else {
        $.get("/users/" + user_id + "/follow");
        t.attr("followed", "true");
      }
      $.users.showFollowButton(t);
    });
  },

  showInModalList: function(element){
    var t = $(element);
    t.find("a[data-toggle='follow-button']").each(function(){
      $.users.showFollowButton(this);
    });
  },

  showInSidebarList: function(element){
    var t = $(element);
    t.find("a[data-toggle='follow-button']").each(function(){
      $.users.showFollowButton(this);
    });
  }
};

$.fn.showModalListUser = function(){
  $.users.showInModalList(this);
};

$.fn.showSidebarListUser = function(){
  $.users.showInSidebarList(this);
};
