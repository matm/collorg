<map version="0.9.0">
<!-- To view this file, download free mind mapping software FreeMind from http://freemind.sourceforge.net -->
<node CREATED="1323841164709" ID="ID_1154347970" MODIFIED="1324042781395" TEXT="depoZ">
<node CREATED="1323841867391" FOLDED="true" ID="ID_1615078451" MODIFIED="1324042344853" POSITION="right" TEXT="actor">
<node CREATED="1323941380485" ID="ID_1223440411" MODIFIED="1323951294556">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      The actor package provides the informations concerning the different persons involved in the organization and the classification relevent for the organization (see category and role)
    </p>
  </body>
</html></richcontent>
<icon BUILTIN="edit"/>
</node>
<node CREATED="1323842111487" FOLDED="true" ID="ID_675824184" MODIFIED="1324042254476" TEXT="person">
<icon BUILTIN="male1"/>
<node CREATED="1323951342590" ID="ID_42100402" MODIFIED="1323952027121">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      Anyone must be identified to trigger an action on the application, appart for the actions authorized for anonymous (see actor.role and actor.category).
    </p>
  </body>
</html></richcontent>
</node>
</node>
<node CREATED="1323842135295" FOLDED="true" ID="ID_1425177550" MODIFIED="1324042254478" TEXT="category">
<icon BUILTIN="group"/>
<node CREATED="1323933813267" ID="ID_1502944752" MODIFIED="1324042008764">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      identifies the different categories of actors.
    </p>
    <p>
      Used to <i><b>restrict</b></i>&#160;the roles to certain categories of populations. <i><b>Not realy democratic</b></i>! But we at least need one benevolent dictator of the world! I mean &quot;<u>administrator</u>&quot; here...
    </p>
    <p>
      A person is known to be part of a category if there is a link between that person and the category considered (see the relation actor.r_person_category, not represented here).
    </p>
    <p>
      Two exceptions here: &quot;<u>visitor</u>&quot; and &quot;<u>anonymous</u>&quot; are implicit categories.
    </p>
    <p>
      Is considered &quot;<u>anonymous</u>&quot; anyone not connected who is browsing the site.
    </p>
    <p>
      Any person connected is at least a &quot;<u>visitor</u>&quot;
    </p>
  </body>
</html>
</richcontent>
<icon BUILTIN="edit"/>
</node>
</node>
<node CREATED="1323842076191" FOLDED="true" ID="ID_1432242603" MODIFIED="1324042254479" TEXT="role">
<icon BUILTIN="group"/>
<node CREATED="1323844137793" ID="ID_1393024206" MODIFIED="1323952503207">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      all the roles of the application are here.
    </p>
    <p>
      The following roles are in the application by default :
    </p>
    <ul>
      <li>
        anonymous
      </li>
      <li>
        visitor
      </li>
      <li>
        administrator
      </li>
      <li>
        developer
      </li>
      <li>
        planner
      </li>
    </ul>
    <p>
      A role is attached to one or more categories. A role can be conferred only to persons belonging to the categories attached to the role.
    </p>
    <p>
      The existence of the relation between a role and a category is mandatory for the access.
    </p>
  </body>
</html></richcontent>
<icon BUILTIN="edit"/>
</node>
</node>
</node>
<node CREATED="1323841627807" FOLDED="true" ID="ID_1020598304" MODIFIED="1324042248331" POSITION="right" TEXT="activity">
<node CREATED="1323937799686" ID="ID_1780479296" MODIFIED="1323937802086" TEXT="domain"/>
<node CREATED="1323842333832" ID="ID_1660086431" MODIFIED="1323842338160" TEXT="task"/>
<node CREATED="1323842338976" ID="ID_1920216165" MODIFIED="1323842344817" TEXT="action"/>
<node CREATED="1323937953064" ID="ID_1170773297" MODIFIED="1323938917170" TEXT="event">
<icon BUILTIN="help"/>
<icon BUILTIN="full-1"/>
</node>
<node CREATED="1323937975034" ID="ID_1643248107" MODIFIED="1323939064538" TEXT="scheduler">
<icon BUILTIN="help"/>
<icon BUILTIN="full-1"/>
</node>
<node CREATED="1323952633953" FOLDED="true" ID="ID_641078423" MODIFIED="1324042781393" TEXT="state machine">
<node CREATED="1323952653852" ID="ID_1655444242" MODIFIED="1323952656721" TEXT="state"/>
<node CREATED="1323952657321" ID="ID_1011390465" MODIFIED="1323952660584" TEXT="transition"/>
</node>
</node>
<node CREATED="1323841637567" FOLDED="true" ID="ID_334928346" MODIFIED="1324042775432" POSITION="right" TEXT="organization">
<node CREATED="1323842068304" ID="ID_470667544" MODIFIED="1323933021042" TEXT="unit (abstract)">
<icon BUILTIN="group"/>
</node>
<node CREATED="1324042351679" ID="ID_719278990" MODIFIED="1324042374062" TEXT="unit member"/>
<node CREATED="1323856835852" FOLDED="true" ID="ID_1727737671" MODIFIED="1324042775429" TEXT="unit map (abstract)">
<node CREATED="1323856869787" FOLDED="true" ID="ID_585118307" MODIFIED="1324042775426" TEXT="collaboration">
<node CREATED="1324041464003" ID="ID_1195852051" MODIFIED="1324042404262">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      A collaboration can be between two or more units. We should be able to retreive this information. The same remark can be made for the partnership...
    </p>
  </body>
</html></richcontent>
<icon BUILTIN="help"/>
</node>
</node>
<node CREATED="1323933649156" ID="ID_425726232" MODIFIED="1323933655329" TEXT="partnership"/>
<node CREATED="1323856874197" ID="ID_299781166" MODIFIED="1323856891202" TEXT="dependence"/>
<node CREATED="1323858253524" ID="ID_1953842227" MODIFIED="1323858255449" TEXT="..."/>
</node>
<node CREATED="1323933498221" FOLDED="true" ID="ID_577975705" MODIFIED="1324042775430" TEXT="role map">
<node CREATED="1324042592218" ID="ID_61539681" MODIFIED="1324042699809" TEXT="the hierarchy of the roles in the organization. Usefull to delegate the attribution of roles hence tasks in the application..."/>
</node>
</node>
<node CREATED="1323841863726" FOLDED="true" ID="ID_1733782135" MODIFIED="1324042778397" POSITION="right" TEXT="group">
<node CREATED="1323843301792" FOLDED="true" ID="ID_1634104419" MODIFIED="1324042778396" TEXT="member">
<node CREATED="1323849602591" ID="ID_1738906324" MODIFIED="1323878451836" TEXT="link between an actor.person and a group">
<icon BUILTIN="edit"/>
</node>
</node>
<node CREATED="1323842181375" ID="ID_1889066789" MODIFIED="1323842916820" TEXT="group">
<icon BUILTIN="group"/>
</node>
</node>
<node CREATED="1323842798656" FOLDED="true" ID="ID_248652361" MODIFIED="1324042781395" POSITION="left" TEXT="controller">
<node CREATED="1323849706864" FOLDED="true" ID="ID_1074799926" MODIFIED="1323971743525" TEXT="access">
<node CREATED="1323856063363" ID="ID_1772165395" MODIFIED="1323971738604">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      link between:
    </p>
    <ul>
      <li>
        actor.person
      </li>
      <li>
        organization.role
      </li>
      <li>
        data (core.oid_table)
      </li>
    </ul>
    <p>
      A <u>person</u>&#160;is granted an <u>access</u>&#160;(ie. <i>is allowed to trigger an action on an object</i>) if the given <u>role,</u>&#160;referenced by that access, connects the person to any <u>task</u>&#160;that includes the <u>action</u>.
    </p>
  </body>
</html></richcontent>
<icon BUILTIN="edit"/>
</node>
</node>
<node CREATED="1323937844148" ID="ID_1668161283" MODIFIED="1323937846864" TEXT="presentation"/>
</node>
<node CREATED="1323843503936" FOLDED="true" ID="ID_1676645199" MODIFIED="1323953051538" POSITION="left" TEXT="core">
<node CREATED="1323849714383" FOLDED="true" ID="ID_1652244680" MODIFIED="1323953051535" TEXT="database">
<icon BUILTIN="full-1"/>
<node CREATED="1323855959817" ID="ID_337821802" MODIFIED="1323855988014" TEXT="remote collorg db"/>
</node>
<node CREATED="1323849720079" ID="ID_805271159" MODIFIED="1323857933079" TEXT="schema">
<icon BUILTIN="full-1"/>
</node>
<node CREATED="1323849722991" ID="ID_880547873" MODIFIED="1323857933078" TEXT="table">
<icon BUILTIN="full-1"/>
</node>
<node CREATED="1323849728750" ID="ID_1798527448" MODIFIED="1323857933077" TEXT="field">
<icon BUILTIN="full-1"/>
</node>
<node CREATED="1323849731087" ID="ID_168266706" MODIFIED="1323849739060" TEXT="base table (abstract)"/>
<node CREATED="1323849756302" ID="ID_1749053335" MODIFIED="1323849761827" TEXT="oid table"/>
<node CREATED="1323856955346" FOLDED="true" ID="ID_423820589" MODIFIED="1323953051536" TEXT="entity">
<icon BUILTIN="full-2"/>
<node CREATED="1323857126827" ID="ID_365110663" MODIFIED="1323878436809">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <p>
      An entity is any data of the database.&#160;&#160;A relation could be an entity...
    </p>
  </body>
</html></richcontent>
<icon BUILTIN="edit"/>
</node>
</node>
<node CREATED="1323856961807" ID="ID_1371089910" MODIFIED="1323858830550" TEXT="relation">
<icon BUILTIN="full-2"/>
</node>
<node CREATED="1323857293715" ID="ID_1388915136" MODIFIED="1323858830549" TEXT="relation type">
<icon BUILTIN="full-2"/>
</node>
</node>
<node CREATED="1323938576928" FOLDED="true" ID="ID_1102172970" MODIFIED="1323953051541" POSITION="left" TEXT="documentation">
<node CREATED="1323938589337" ID="ID_47181825" MODIFIED="1323938594548" TEXT="report"/>
<node CREATED="1323938620165" FOLDED="true" ID="ID_1687601043" MODIFIED="1323953051539" TEXT="report category">
<node CREATED="1323940403658" ID="ID_70759449" MODIFIED="1323941160962">
<richcontent TYPE="NODE"><html>
  <head>
    
  </head>
  <body>
    <ul>
      <li>
        help
      </li>
      <li>
        incident notification
      </li>
      <li>
        help request
      </li>
      <li>
        feature request
      </li>
      <li>
        enhancement request
      </li>
      <li>
        ...
      </li>
    </ul>
  </body>
</html></richcontent>
<icon BUILTIN="edit"/>
</node>
</node>
<node CREATED="1323941212248" ID="ID_54739283" MODIFIED="1323941214997" TEXT="ticket"/>
<node CREATED="1323941215848" ID="ID_1283244967" MODIFIED="1323941219806" TEXT="tikcet category"/>
<node CREATED="1323938626946" ID="ID_1520554388" MODIFIED="1323938631801" TEXT="document"/>
<node CREATED="1323941221532" ID="ID_880158118" MODIFIED="1323941226331" TEXT="document category"/>
</node>
<node CREATED="1323938679810" FOLDED="true" ID="ID_237303605" MODIFIED="1323953051542" POSITION="left" TEXT="i18n">
<node CREATED="1323938687128" ID="ID_1687205634" MODIFIED="1323938690766" TEXT="translation"/>
<node CREATED="1323938705671" ID="ID_740520979" MODIFIED="1323938707631" TEXT="language"/>
</node>
<node CREATED="1323937816292" FOLDED="true" ID="ID_1772105717" MODIFIED="1323971913434" POSITION="left" TEXT="web">
<node CREATED="1323938653599" ID="ID_380827289" MODIFIED="1323938656831" TEXT="page"/>
<node CREATED="1323938657612" ID="ID_1824367779" MODIFIED="1323938658991" TEXT="url"/>
<node CREATED="1323938659315" ID="ID_1765220897" MODIFIED="1323971866115" TEXT="topic"/>
</node>
</node>
</map>
