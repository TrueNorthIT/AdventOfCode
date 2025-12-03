DROP TABLE dbo.Banks
CREATE TABLE dbo.Banks
(
    Bank NVARCHAR (100) NOT NULL,
);

--paste your input into this section
INSERT INTO dbo.Banks
VALUES	
	('987654321111111'),
	('811111111111119'),
	('234234234234278'),
	('818181911112111');

with solve(part, n, bank, joltage)
as ((	
		select 'p1', 2, bank, CAST('' as varchar) from banks
		union
		select 'p2', 12, bank, CAST('' as varchar) from banks
	)
	union all
	select
		part,
		n - 1,
		SUBSTRING(bank, i + 1, LEN(bank) - i),
		CAST(joltage + SUBSTRING(bank, i, 1) as varchar)
		from
		(
			select *,
			IIF(i9 > 0 and i9 <= max, i9,
			 IIF(i8 > 0 and i8 <= max, i8,
			  IIF(i7 > 0 and i7 <= max, i7,
			   IIF(i6 > 0 and i6 <= max, i6,
			    IIF(i5 > 0 and i5 <= max, i5,
			     IIF(i4 > 0 and i4 <= max, i4,
			      IIF(i3 > 0 and i3 <= max, i3,
			       IIF(i2 > 0 and i2 <= max, i2,
			        IIF(i1 > 0 and i1 <= max, i1,
			0))))))))) as i
			from
			(
				select *,
				CHARINDEX('9', bank) as i9,
				CHARINDEX('8', bank) as i8,
				CHARINDEX('7', bank) as i7,
				CHARINDEX('6', bank) as i6,
				CHARINDEX('5', bank) as i5,
				CHARINDEX('4', bank) as i4,
				CHARINDEX('3', bank) as i3,
				CHARINDEX('2', bank) as i2,
				CHARINDEX('1', bank) as i1,
				LEN(bank) - n + 1 as max
				from solve
				where n > 0
			) q1
		) q2
)
select part, SUM(CAST(joltage as bigint)) as answer from solve
where n = 0
group by part