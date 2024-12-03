
function toggleGroup(userId, groupId, isInGroup) {
    const action = isInGroup === 'true' ? 'remove' : 'add';
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = window.location.href;

    const userInput = document.createElement('input');
    userInput.type = 'hidden';
    userInput.name = 'user_id';
    userInput.value = userId;

    const groupInput = document.createElement('input');
    groupInput.type = 'hidden';
    groupInput.name = 'group_id';
    groupInput.value = groupId;

    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action';
    actionInput.value = action;

    form.appendChild(userInput);
    form.appendChild(groupInput);
    form.appendChild(actionInput);
    
    document.body.appendChild(form);
    form.submit();
}

