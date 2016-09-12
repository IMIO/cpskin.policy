*** Keywords ***

Créer sous-niveaux
    ${niv2}=  path to uid  plone/ma-commune/services-communaux
    ${niv2}=  Run keyword if  '${niv2}' == 'None'  Créer dossier et publier dans la navigation  services-communaux  Services communaux  plone/ma-commune  ELSE  Get variable value  ${niv2}
    ${niv3}=  path to uid  plone/ma-commune/services-communaux/informatique
    ${niv3}=  Run keyword if  '${niv3}' == 'None'  Créer dossier et publier dans la navigation  informatique  Informatique  ${niv2}  ELSE  Get variable value  ${niv3}

Créer dossier et publier dans la navigation
    [Arguments]  ${id}  ${title}  ${container}
    ${uid}=  create content  type=Folder  id=${id}  title=${title}  container=${container}
    Fire transition  ${uid}  publish_and_show
    Return from keyword  Get variable value  ${uid}
    