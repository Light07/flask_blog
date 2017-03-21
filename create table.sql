create database kevin_forum


use kevin_forum
go



create table Role(
RoleId int not null IDENTITY(1,1) primary key,
RoleName nvarchar(50) not null, 
Description nvarchar(100) 
)

create table Privilege(
PrivilegeId int not null IDENTITY(1,1) primary key, 
PrivilegeName nvarchar(50) not null, 
Description nvarchar(100)
)

create table RolePrivilege(
RolePrivilegeId int not null IDENTITY(1,1) primary key,
RoleId int not null  foreign key references Role(RoleId),
PrivilegeIdRoleIdMap nvarchar(max) not null
)



create table Members(
MemberId int not null  IDENTITY(1,1) primary key, 
UserName nvarchar(50) unique NOT NULL, 
PassWord nvarchar(50) not null, 
RoleId int not null  default(2) foreign key references Role(RoleId),
PhoneNumber nvarchar(50) unique NOT NULL
)


CREATE TABLE [dbo].[Categories](
	[CId] [int] IDENTITY(1,1) NOT NULL primary key,
	[CName] [nvarchar](100) NOT NULL,
)

CREATE TABLE [dbo].[Posts](
	[PId] [int] IDENTITY(1,1) NOT NULL PRIMARY KEY,
	[Title] [nvarchar](100) NULL,
	[Contents] [nvarchar](max) NULL,
	[MemberId] [int] NOT NULL foreign key references Members(MemberId),
	[CId] [int] NOT NULL,
	[Comments] [nvarchar](max) NULL,
	[ShownPost] bit NOT NULL DEFAULT(1),
	[InsertTime] [datetime]  DEFAULT(getdate()),
	[ModifyTime] [datetime]  DEFAULT(getdate()),
	[ModifyByMemberId] [int] NULL
	
)

alter table [dbo].[Posts]
add constraint posts_members_conn foreign key(MemberId) references [dbo].[Members](MemberId) 

alter table [dbo].[Posts]
add foreign key(CId) references [dbo].[Categories](CId) 

