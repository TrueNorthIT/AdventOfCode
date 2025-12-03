if exists (select * from sys.tables where object_id = OBJECT_ID('dbo.inputsample'))
exec sp_executesql 'DROP TABLE dbo.inputsample'
GO
create table dbo.input (
[id] int identity(1, 1) primary key,
[puzzle] varchar(100) not null,
--[FirstDigit] int NULL,
--[FirstDigitIndex] int NULL,
--[SecondDigit] int NULL,
)
GO
