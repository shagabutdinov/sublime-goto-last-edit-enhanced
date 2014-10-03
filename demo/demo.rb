class CommentController < ApplicationController

  def create()
    comment = Comment.create(
      sender_id: _user_id,
      point_id: params[:point_id],
      text: params[:text],
      file: params[:file]
    )

    comment.save()

    should_notify = comment.project.owner.name != 'Unregistered' &&
      comment.point.task.folder.project.email_notifications

    if should_notify
      CommentMailer.new_comment_notification(comment).deliver()
    end

    @user = User.find(_user_id)
    return render(partial: 'workspace/comment', locals: {comment: comment,
      point: nil}, formats: [:html])
  end

end