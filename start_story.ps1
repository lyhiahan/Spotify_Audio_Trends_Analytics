# Run from any folder; a separate port keeps the original dashboard available.
$storyProject = $PSScriptRoot
Set-Location -LiteralPath $storyProject
python -m streamlit run dashboard/story_app.py --server.port 8502 --server.address 127.0.0.1 --theme.base light --browser.gatherUsageStats false
