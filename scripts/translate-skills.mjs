import fs from 'fs';
import path from 'path';

async function translateText(text) {
  if (!text.trim() || text.match(/^[#\-\s]+$/)) return text;
  try {
    const url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=es&dt=t&q=' + encodeURIComponent(text);
    const res = await fetch(url);
    const json = await res.json();
    return json[0].map(x => x[0]).join('');
  } catch (e) {
    return text;
  }
}

async function translateFile(sourcePath, targetPath) {
  const content = fs.readFileSync(sourcePath, 'utf8');
  console.log('Translating ' + sourcePath + '...');
  let lines = content.split('\n');
  let translatedLines = [];
  let inFrontmatter = false;
  let chunk = [];
  
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (i === 0 && line.trim() === '---') {
      inFrontmatter = true;
      translatedLines.push(line);
      continue;
    }
    if (inFrontmatter && line.trim() === '---') {
      inFrontmatter = false;
      translatedLines.push(line);
      continue;
    }
    if (inFrontmatter) {
      if (line.startsWith('description: ')) {
        const desc = line.replace('description: ', '');
        const trans = await translateText(desc);
        translatedLines.push('description: ' + trans);
      } else {
        translatedLines.push(line);
      }
      continue;
    }
    if (line.trim() === '') {
      if (chunk.length > 0) {
        const textToTrans = chunk.join('\n');
        if (textToTrans.startsWith('```') || textToTrans.startsWith('    ')) {
           translatedLines.push(textToTrans);
        } else {
           const translated = await translateText(textToTrans);
           translatedLines.push(translated);
        }
        chunk = [];
      }
      translatedLines.push('');
    } else {
      chunk.push(line);
    }
  }
  if (chunk.length > 0) {
      const textToTrans = chunk.join('\n');
      if (textToTrans.startsWith('```') || textToTrans.startsWith('    ')) {
         translatedLines.push(textToTrans);
      } else {
         const translated = await translateText(textToTrans);
         translatedLines.push(translated);
      }
  }
  const finalContent = translatedLines.join('\n').replace(/\] \(/g, '](').replace(/# #/g, '##').replace(/# # #/g, '###').replace(/# # # #/g, '####');
  fs.writeFileSync(targetPath, finalContent);
  console.log('Saved ' + targetPath);
}

async function main() {
  const skillsDir = path.join(process.cwd(), 'skills');
  const items = fs.readdirSync(skillsDir, { withFileTypes: true });
  const tasks = [];

  for (const item of items) {
    if (item.isDirectory()) {
      const dirPath = path.join(skillsDir, item.name);
      const enFile = path.join(dirPath, 'SKILL.md');
      const esFile = path.join(dirPath, 'SKILL_es.md');

      if (fs.existsSync(enFile) && !fs.existsSync(esFile)) {
        tasks.push(() => translateFile(enFile, esFile));
      }
    }
  }
  
  // Throttle to 15 concurrent
  for (let i = 0; i < tasks.length; i += 15) {
      const batch = tasks.slice(i, i + 15).map(t => t());
      await Promise.all(batch);
  }
}

main().catch(console.error);
