[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$Path,

    [Parameter(Mandatory = $true)]
    [ValidateRange(1, 999)]
    [int]$ChapterNumber,

    [int]$ExpectedSections = -1,
    [int]$ExpectedSubsections = -1,
    [int]$ExpectedEquations = -1,
    [int]$ExpectedFigures = -1,
    [int]$ExpectedExamples = -1,
    [int]$ExpectedExercises = -1,
    [int]$ExpectedLemmas = -1,
    [int]$ExpectedFootnotes = -1
)

$resolvedAuditPath = (Resolve-Path -LiteralPath $Path -ErrorAction Stop).Path
$auditText = Get-Content -LiteralPath $resolvedAuditPath -Raw -Encoding UTF8

function Get-MatchCount {
    param([string]$Pattern)
    return ([regex]::Matches($auditText, $Pattern, [System.Text.RegularExpressions.RegexOptions]::Multiline)).Count
}

$chapterPattern = [regex]::Escape("eq:$ChapterNumber.") + '(\d+)'
$equationMatches = [regex]::Matches($auditText, '\\label\{' + $chapterPattern + '\}')
$equationNumbers = @($equationMatches | ForEach-Object { [int]$_.Groups[1].Value })
$uniqueEquationNumbers = @($equationNumbers | Sort-Object -Unique)
$missingEquationNumbers = @()

if ($uniqueEquationNumbers.Count -gt 0) {
    $minimumEquationNumber = ($uniqueEquationNumbers | Measure-Object -Minimum).Minimum
    $maximumEquationNumber = ($uniqueEquationNumbers | Measure-Object -Maximum).Maximum
    $missingEquationNumbers = @($minimumEquationNumber..$maximumEquationNumber | Where-Object { $_ -notin $uniqueEquationNumbers })
}

$auditCounts = [ordered]@{
    chapters = Get-MatchCount '^\\chapter\{'
    sections = Get-MatchCount '^\\section\{'
    subsections = Get-MatchCount '^\\subsection\{'
    formal_subsubsections = Get-MatchCount '^\\subsubsection\{'
    equation_labels = $equationNumbers.Count
    unique_equation_labels = $uniqueEquationNumbers.Count
    figures = Get-MatchCount '\\label\{fig:' + [regex]::Escape("$ChapterNumber.") + '\d+\}'
    examples = Get-MatchCount '^\\begin\{example\}'
    exercises = Get-MatchCount '^\\begin\{exercise\}'
    lemmas = Get-MatchCount '^\\begin\{lemma\*?\}'
    footnotes = Get-MatchCount '\\footnote\{'
}

$auditExpectations = [ordered]@{
    sections = $ExpectedSections
    subsections = $ExpectedSubsections
    equation_labels = $ExpectedEquations
    figures = $ExpectedFigures
    examples = $ExpectedExamples
    exercises = $ExpectedExercises
    lemmas = $ExpectedLemmas
    footnotes = $ExpectedFootnotes
}

$auditFailures = [System.Collections.Generic.List[string]]::new()

foreach ($auditKey in $auditExpectations.Keys) {
    $expectedValue = $auditExpectations[$auditKey]
    if ($expectedValue -ge 0 -and $auditCounts[$auditKey] -ne $expectedValue) {
        $auditFailures.Add("$auditKey expected $expectedValue but found $($auditCounts[$auditKey])")
    }
}

if ($equationNumbers.Count -ne $uniqueEquationNumbers.Count) {
    $auditFailures.Add('equation labels are duplicated')
}

if ($missingEquationNumbers.Count -gt 0) {
    $auditFailures.Add("equation sequence has gaps: $($missingEquationNumbers -join ', ')")
}

$forbiddenPatterns = [ordered]@{
    atop = '\\atop'
    comment_block = '\\begin\{comment\}'
}

$forbiddenFindings = [ordered]@{}
foreach ($forbiddenKey in $forbiddenPatterns.Keys) {
    $forbiddenCount = Get-MatchCount $forbiddenPatterns[$forbiddenKey]
    $forbiddenFindings[$forbiddenKey] = $forbiddenCount
    if ($forbiddenCount -gt 0) {
        $auditFailures.Add("forbidden pattern $forbiddenKey found $forbiddenCount time(s)")
    }
}

$auditResult = [ordered]@{
    path = $resolvedAuditPath
    chapter_number = $ChapterNumber
    counts = $auditCounts
    equation_sequence = [ordered]@{
        minimum = if ($uniqueEquationNumbers.Count -gt 0) { $uniqueEquationNumbers[0] } else { $null }
        maximum = if ($uniqueEquationNumbers.Count -gt 0) { $uniqueEquationNumbers[-1] } else { $null }
        missing = $missingEquationNumbers
    }
    forbidden_findings = $forbiddenFindings
    passed = ($auditFailures.Count -eq 0)
    failures = @($auditFailures)
}

$auditResult | ConvertTo-Json -Depth 6

if ($auditFailures.Count -gt 0) {
    exit 1
}
