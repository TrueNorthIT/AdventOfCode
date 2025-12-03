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

create function dbo.get_Power2(@input VARCHAR(100)) RETURNS BIGINT
AS
BEGIN
	declare @index1 int	
	declare @index2 int	
	declare @index3 int	
	declare @index4 int	
	declare @index5 int	
	declare @index6 int	
	declare @index7 int	
	declare @index8 int	
	declare @index9 int	
	declare @index10 int	
	declare @index11 int	
	declare @index12 int	
	set @index1 = dbo.get_GetFirstIndexOfHighest(@input, 1, LEN(@input)-11)
	set @index2 = dbo.get_GetFirstIndexOfHighest(@input, @index1 + 1, LEN(@input)-10)
	set @index3 = dbo.get_GetFirstIndexOfHighest(@input, @index2 + 1, LEN(@input)-9)
	set @index4 = dbo.get_GetFirstIndexOfHighest(@input, @index3 + 1, LEN(@input)-8)
	set @index5 = dbo.get_GetFirstIndexOfHighest(@input, @index4 + 1, LEN(@input)-7)
	set @index6 = dbo.get_GetFirstIndexOfHighest(@input, @index5 + 1, LEN(@input)-6)
	set @index7 = dbo.get_GetFirstIndexOfHighest(@input, @index6 + 1, LEN(@input)-5)
	set @index8 = dbo.get_GetFirstIndexOfHighest(@input, @index7 + 1, LEN(@input)-4)
	set @index9 = dbo.get_GetFirstIndexOfHighest(@input, @index8 + 1, LEN(@input)-3)
	set @index10 = dbo.get_GetFirstIndexOfHighest(@input, @index9 + 1, LEN(@input)-2)
	set @index11 = dbo.get_GetFirstIndexOfHighest(@input, @index10 + 1, LEN(@input)-1)
	set @index12 = dbo.get_GetFirstIndexOfHighest(@input, @index11 + 1, LEN(@input))
	return CONVERT(bigint, 
		substring(@input, @index1,1) 
		+ substring(@input, @index2,1)
		+ substring(@input, @index3,1)
		+ substring(@input, @index4,1)
		+ substring(@input, @index5,1)
		+ substring(@input, @index6,1)
		+ substring(@input, @index7,1)
		+ substring(@input, @index8,1)
		+ substring(@input, @index9,1)
		+ substring(@input, @index10,1)
		+ substring(@input, @index11,1)
		+ substring(@input, @index12,1)
	)
END
GO

select dbo.get_Power2('818181911112111')

select sum(dbo.get_Power2([puzzle])) from dbo.input