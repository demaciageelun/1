{'data': {'formInfo': {'widgetMap': {
    '_S_INT_LEAVE_REASON': {'codeId': '_S_INT_LEAVE_REASON', 'extendFieldMap': {}, 'title': '请假事由',
                            'type': 'textAreaWidget', 'value': ''},
    '_S_INT_LEAVE_DESC': {'codeId': '_S_INT_LEAVE_DESC', 'describeFileVos': [], 'extendFieldMap': {}, 'title': '说明文字',
                          'type': 'describeWidget'},
    'Te_0': {'codeId': 'Te_0', 'extendFieldMap': {'wordLimit': 200}, 'title': '工号', 'type': 'textWidget',
             'value': '20080103'}, 'Ra_0': {'codeId': 'Ra_0', 'extendFieldMap': {}, 'displaylinkageVos': [{
                                                                                                              'additional': {
                                                                                                                  'state': {
                                                                                                                      'label': '必填',
                                                                                                                      'value': 'required'},
                                                                                                                  'option': [
                                                                                                                      {
                                                                                                                          'label': '生产/品保/仓储一线人员',
                                                                                                                          'value': 'AaBaCcDd'}],
                                                                                                                  'target': {
                                                                                                                      'label': '班组长',
                                                                                                                      'value': 'Ps_0'}},
                                                                                                              'rule': {
                                                                                                                  'or': [
                                                                                                                      {
                                                                                                                          'eq': 'AaBaCcDd'}]},
                                                                                                              'behavior': {
                                                                                                                  'Ps_0': {
                                                                                                                      'state': 'required'}}},
                                                                                                          {
                                                                                                              'additional': {
                                                                                                                  'state': {
                                                                                                                      'label': '隐藏',
                                                                                                                      'value': 'hidden'},
                                                                                                                  'option': [
                                                                                                                      {
                                                                                                                          'label': '非一线人员',
                                                                                                                          'value': 'EeFfGgHh'}],
                                                                                                                  'target': {
                                                                                                                      'label': '班组长',
                                                                                                                      'value': 'Ps_0'}},
                                                                                                              'rule': {
                                                                                                                  'or': [
                                                                                                                      {
                                                                                                                          'eq': 'EeFfGgHh'}]},
                                                                                                              'behavior': {
                                                                                                                  'Ps_0': {
                                                                                                                      'state': 'hidden'}}}],
                                            'options': [{'checked': "False", 'value': '生产/品保/仓储一线人员', 'key': 'AaBaCcDd'},
                                                        {'checked': "False", 'value': '非一线人员', 'key': 'EeFfGgHh'}],
                                            'linkRule': [], 'title': '请假人员类别', 'type': 'radioWidget',
                                            'value': 'EeFfGgHh'}, '_S_APPLY': {'eid': '19469603', 'codeId': '_S_APPLY',
                                                                               'assignRule': [{'codeId': 'Te_0',
                                                                                               'fieldSubTypeName': '',
                                                                                               'infoType': 'DEFAULT',
                                                                                               'readonly': "False",
                                                                                               'dicId': '',
                                                                                               'widgetTypeName': '单行文本框',
                                                                                               'fieldSubType': '',
                                                                                               'title': '企业工号',
                                                                                               'key': 'jobNo',
                                                                                               'widgetType': 'textWidget'}],
                                                                               'extendFieldMap': {},
                                                                               'existEcosphere': "False",
                                                                               'optSource': 'org', 'title': '提交人',
                                                                               'type': 'personSelectWidget',
                                                                               'personInfo': [{
                                                                                                  'image': 'https://static.yunzhijia.com/space/c/photo/load?id=60d59879fc15d6000143ffae',
                                                                                                  'companyName': '江苏谷登重型机械装备科技有限公司',
                                                                                                  'jobTitle': 'ERP专员',
                                                                                                  'name': '周为',
                                                                                                  'deptLongName': '江苏谷登重型机械装备科技有限公司/运营中心/信息化部',
                                                                                                  'oid': '5f2e53bce4b0ce6aad23fa1e',
                                                                                                  'dept': '信息化部',
                                                                                                  'userId': '5f2686c2e4b0aa487b634a9c'}],
                                                                               'value': ['5f2e53bce4b0ce6aad23fa1e']},
    'Ps_0': {'eid': '19469603', 'codeId': 'Ps_0', 'roleIds': [], 'extendFieldMap': {}, 'existEcosphere': "False",
             'optSource': 'org', 'title': '班组长', 'type': 'personSelectWidget', 'personInfo': [], 'option': 'single'},
    '_S_URGENCY_DEGREE': {'codeId': '_S_URGENCY_DEGREE', 'extendFieldMap': {}, 'displaylinkageVos': [],
                          'options': [{'checked': "True", 'value': '普通', 'key': '1'},
                                      {'checked': "False", 'value': '紧急', 'key': '2'},
                                      {'checked': "False", 'value': '加急', 'key': '3'},
                                      {'checked': "False", 'value': '特急', 'key': '4'},
                                      {'checked': "False", 'value': '特提', 'key': '5'}], 'linkRule': [], 'title': '紧急程度',
                          'type': 'radioWidget', 'value': '1'},
    '_S_SERIAL': {'codeId': '_S_SERIAL', 'extendFieldMap': {}, 'title': '流水号', 'type': 'serialNumWidget',
                  'value': 'CSQJSQD-20210923-004'},
    '_S_DATE': {'codeId': '_S_DATE', 'fromNowOn': "False", 'title': '申请日期', 'type': 'dateWidget', 'value': 1632382543308},
    'Im_0': {'codeId': 'Im_0', 'extendFieldMap': {}, 'maximum': 200, 'title': '图片', 'type': 'imageWidget', 'value': []},
    'At_0': {'codeId': 'At_0', 'extendFieldMap': {}, 'maximum': 200, 'title': '文件', 'type': 'attachmentWidget',
             'value': []},
    '_S_DEPT': {'eid': '19469603', 'codeId': '_S_DEPT', 'title': '所属部门', 'type': 'departmentSelectWidget', 'deptInfo': [
        {'name': '信息化部', 'orgId': '4eebc4b6-0c4e-11ec-8a77-ecf4bbea1498', 'realLongName': '江苏谷登重型机械装备科技有限公司!运营中心!信息化部',
         'longName': '信息化部(运营中心)'}], 'selectCompanyOnly': "False", 'value': ['4eebc4b6-0c4e-11ec-8a77-ecf4bbea1498']},
    '_S_TITLE': {'codeId': '_S_TITLE', 'extendFieldMap': {'titleEntity': {'kind': 'TITLE_DEFAULT', 'list': [
        {'formItem': '_S_APPLY', 'kind': 'ITEM_FORM_ITEM'}, {'formItem': '的', 'kind': 'ITEM_STRING'},
        {'formItem': '模板名称', 'kind': 'ITEM_TEMPLATENAME'}]}, 'defaultTitle': "True"}, 'title': '标题', 'type': 'textWidget',
                 'value': '周为的测试请假申请单'}}, 'detailMap': {
    '_S_INT_LEAVE_DETAILED': {'buttonName': '添加请假明细', 'codeId': '_S_INT_LEAVE_DETAILED', 'widgetVos': {
        '_S_INT_LEAVE_TYPE': {'codeId': '_S_INT_LEAVE_TYPE', 'extendFieldMap': {}, 'displaylinkageVos': [],
                              'options': [], 'linkRule': [], 'title': '请假类型', 'type': 'radioWidget'},
        '_S_INT_LEAVE_TIME': {'codeId': '_S_INT_LEAVE_TIME', 'dateFormat': 'yyyy-MM-dd HH:mm', 'extendFieldMap': {},
                              'fromNowOn': "False", 'title2': '结束时间', 'title': '开始时间', 'type': 'dateRangeWidget'},
        '_S_INT_LEAVE_DAYS': {'codeId': '_S_INT_LEAVE_DAYS', 'decimalDigit': 2, 'extendFieldMap': {},
                              'detailCountName': '请假总天数', 'title': '请假天数', 'type': 'numberWidget', 'detailCount': "True"},
        '_S_INT_LEAVE_HOURS': {'codeId': '_S_INT_LEAVE_HOURS', 'decimalDigit': 2, 'extendFieldMap': {},
                               'detailCountName': '请假总时长', 'title': '时长(小时)', 'type': 'numberWidget',
                               'detailCount': "True"}}, 'extendFieldMap': {}, 'lineAttr': [
        {'_S_INT_LEAVE_TIME': {'dateFormat': 'yyyy-MM-dd HH:mm'}, '_S_INT_LEAVE_HOURS': {}}], 'widgetValue': [
        {'_S_INT_LEAVE_TYPE': '5f212e529b3004000175dccd', '_S_INT_LEAVE_TIME': [1632412800000, 1632585600000],
         '_id_': '1', '_S_INT_LEAVE_DAYS': '2', '_S_INT_LEAVE_HOURS': '16'}], 'imageInfo': {}, 'title': '请假信息',
                              'type': 'detailedWidget'}}},
          'basicInfo': {'nodeName': '完成审批', 'eid': '19469603', 'eventId': '8ff605c7-a9df-460d-91a6-57284f705d83',
                        'formDefId': '614c2df99302a400012cf168', 'dataType': 1,
                        'myNetworkInfo': {'eid': '19469603', 'name': '江苏谷登重型机械装备科技有限公司'}, 'nodeType': 'END',
                        'title': '测试请假申请单', 'flowInstId': '614c2e4f7e7e9e000117c170',
                        'formCodeId': '837f79ad8c994bccac7bb817e08b7f08', 'actionType': 'reach', 'myPersonInfo': {
                  'image': 'https://static.yunzhijia.com/space/c/photo/load?id=60d59879fc15d6000143ffae',
                  'jobNo': '20080103', 'name': '周为', 'oid': '5f2e53bce4b0ce6aad23fa1e'},
                        'formInstId': '614c2e4fbfe8ef0001b4f0ee', 'eventTime': 1632382543897,
                        'myDeptInfo': {'name': '信息化部', 'orgId': '4eebc4b6-0c4e-11ec-8a77-ecf4bbea1498'},
                        'interfaceId': 'jsrgHZxz', 'interfaceName': '请假', 'returned': "False",
                        'nodeId': '614c2e4f7e7e9e000117c190'}}, 'success': "True", 'errorCode': 0}
