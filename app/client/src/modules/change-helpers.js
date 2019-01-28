
/*
  User store
 */

const getRoles = function (included) {
  return  included.filter(item => item.type === 'user_role').map(role => { return { id: role.id, ...role.attributes }});
};


export  {

  /* user */
  getRoles,
}
