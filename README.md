# cv-for-nasal-pain-assay
Tools and scripts to automate Computer Vision-based analysis of spontaneous nasal pain after intranasal immune compound injection

## Workflow
1. Collect behavior video as single MP4
2. "split.py": Apply split.py to video to automatically clip video into uniform segments within the byte limit for PainFace
3. Manually upload mp4 files that download from running split.py on full MP4 video to PainFace
4. Manually download folders of results from PainFace
5. "merge.py": Merge important information from CSV files across multiple folders by providing name of root directory
6. "analyze.py": Run data analysis pipeline on consolidated data matrix of full video
7. "plot.py": Produce figures

## Instructions
python3 main.py [args]

## Reminders
Do not push files containing data or files containing outputs from runs with data to GitHub. Clear all outputs from ipynb.
Remove CSV files and MP4 files that download or have been imported to this directory. Move to a separate local directory
to not lose data.
