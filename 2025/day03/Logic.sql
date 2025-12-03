create function dbo.get_GetFirstIndexOfHighest(@input VARCHAR(100), @startIndex INT, @ltethan INT) RETURNS INT
AS
BEGIN
	declare @index int
	set @index = CHARINDEX('9', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('8', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('7', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('6', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('5', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('4', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('3', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('2', @input, @startIndex)
	if @index != 0 and @index <= @ltethan
	  RETURN @index
	set @index = CHARINDEX('1', @input, @startIndex)
	RETURN @index
END
GO

create function dbo.get_Power(@input VARCHAR(100)) RETURNS INT
AS
BEGIN
	declare @firstIndex int	
	declare @secondIndex int	
	set @firstIndex = dbo.get_GetFirstIndexOfHighest(@input, 1, LEN(@input)-1)
	set @secondIndex = dbo.get_GetFirstIndexOfHighest(@input, @firstIndex + 1, LEN(@input))
	return CONVERT(int, substring(@input, @firstIndex,1) + substring(@input, @secondIndex,1))
END
GO

select sum(dbo.get_Power([puzzle])) from dbo.inputsample