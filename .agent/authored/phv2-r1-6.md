9. Authored-text application is verified against the committed
   `.agent/authored/<feature>-r<round>-<n>.md` file (the worker's saved
   copy of your paste), never against your own retype. Every authored
   block you emit carries `sha256=<hex>` of its exact bytes in the BEGIN
   marker so the worker can verify receipt before saving (R-0148).
   Order the disk-to-disk comparison; a proof computed against a
   reconstructed copy is a false verification claim (R-0147 class).
