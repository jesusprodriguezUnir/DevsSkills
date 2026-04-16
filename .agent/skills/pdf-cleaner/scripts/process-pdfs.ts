import { processPDFs, ProcessResult } from '../../../../src/lib/pdf-processor';

async function run() {
  console.log('--- Iniciando Procesamiento de PDFs ---');
  const results: ProcessResult[] = await processPDFs();
  
  const successCount = results.filter((r: ProcessResult) => r.success).length;
  console.log(`Completado: ${successCount} éxitos, ${results.length - successCount} errores.`);
  
  results.forEach((r: ProcessResult) => {
    if (r.success) {
      console.log(`[OK] ${r.fileName} -> ${r.outputPath}`);
    } else {
      console.log(`[ERR] ${r.fileName}: ${r.error}`);
    }
  });
}

run().catch(console.error);
