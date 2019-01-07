from rest_framework.permissions import BasePermission

class IsAddedBy(BasePermission):
	message = "This view is only accessible to admin or the person who added the item "

	def has_object_permission(self, request, view, obj):
		if obj.added_by == request.user:
			return True 
		else: 
			return False