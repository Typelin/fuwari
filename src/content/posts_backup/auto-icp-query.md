---
title: 全自动ICP查询API
published: 2025-09-12T04:50:10
description: '突然听到个很有意思的项目：自动ICP查询，搜集了一下市面上的轮子然后改改，嗯！能用了！'
image: '../assets/images/2025-09-12-04-52-16-image.png'
tags: [ICP]

draft: false 
lang: ''
---

# 原理

由 [ravizhan/ICP-spider: 基于yolov8+孪生网络识别验证码的ICP备案查询程序。从工业和信息化部政务服务平台查询实时数据，高精度过验证码](https://github.com/ravizhan/ICP-spider) 提供图形验证码支持

因为验证码识别成功后得到的Token有效时间大概为30s，此期间无需再次重新识别，故开发一个Token生命周期管理器，后台始终维护有效的Token，用户查询时直接使用有效的Token查询，方便快速

# 使用

查询 qq.com 的ICP备案信息：

http://icp.2x.nz/?domain=qq.com

理应返回如下信息，若未返回结果，则刚好Token失效且生命周期管理器正在获取新的Token，等待几秒后再次查询即可

```json
{
  "code": 200,
  "msg": "操作成功",
  "params": {
    "endRow": 0,
    "hasNextPage": false,
    "hasPreviousPage": false,
    "isFirstPage": true,
    "isLastPage": true,
    "list": [
      {
        "contentTypeName": "文化、文化、宗教、出版、文化、新闻、文化、宗教、宗教、出版",
        "domain": "qq.com",
        "domainId": 190000203203,
        "leaderName": "",
        "limitAccess": "否",
        "mainId": 547280,
        "mainLicence": "粤B2-20090059",
        "natureName": "企业",
        "serviceId": 4134047,
        "serviceLicence": "粤B2-20090059-5",
        "unitName": "深圳市腾讯计算机系统有限公司",
        "updateRecordTime": "2022-09-06 15:51:52"
      }
    ],
    "navigateFirstPage": 1,
    "navigateLastPage": 1,
    "navigatePages": 8,
    "navigatepageNums": [
      1
    ],
    "nextPage": 0,
    "pageNum": 1,
    "pageSize": 10,
    "pages": 1,
    "prePage": 0,
    "size": 1,
    "startRow": 0,
    "total": 1
  },
  "success": true
}
```
