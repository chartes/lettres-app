const getCorrespondents = function (included) {

    const hasRoleById = {};
    const rolesById = {};
    const correspondentsById = {};
    included.forEach(inc => {
      if (inc.type === 'correspondent') {
        correspondentsById[inc.id] = {...inc.attributes}
      } else if (inc.type === 'correspondent-role') {
        rolesById[inc.id] = {...inc.attributes}
      } else if (inc.type === 'correspondent-has-role') {
        hasRoleById[inc.id] = {
          relationId: inc.id,
          roleId: inc.relationships['correspondent-role'].data.id,
          correspondentId: inc.relationships.correspondent.data.id,
        }
      }
    });
    return Object.values(hasRoleById).map(hasRole => { return {
        ...hasRole, correspondent: correspondentsById[hasRole.correspondentId], role: rolesById[hasRole.roleId]
    }})

  },

  getInstitution = function (included) {
    return getSimpleRelation('institution', included)
  },

  getWhitelist = function (included) {
    return getSimpleRelation('whitelist', included)
  },

  getLanguages = function (included) {
    return  included.filter(item => item.type === 'language').map(lang => { return { id: lang.id, ...lang.attributes }});
  },

  getWitnesses = function (included) {
    return  included.filter(item => item.type === 'witness').map(wit => { return { id: wit.id, ...wit.attributes }});
  },

  getCollections = function (included) {
    return  included.filter(item => item.type === 'collection').map(collection => { return { id: collection.id, ...collection.attributes }});
  },

  getNotes = function (included) {
    return  included.filter(item => item.type === 'note').map(lang => { return { id: lang.id, ...lang.attributes }});
  },

  getSimpleRelation = function (propName, included) {
    let found = included.find(item => item.type === propName);
    return found ? { id: found.id, ...found.attributes} : {id: null}
  },

  /*
    User store
   */

  getRoles = function (included) {
    return  included.filter(item => item.type === 'user_role').map(role => { return { id: role.id, ...role.attributes }});
  };


export  {
  getCorrespondents,
  getInstitution,
  getLanguages,
  getWitnesses,
  getNotes,
  getCollections,
  getRoles
}
