import { exec } from 'child_process';

export default function handler(req, res) {
  // Check for authorization if you've set up a CRON_SECRET environment variable
  if (req.headers.get('Authorization') !== `Bearer ${process.env.CRON_SECRET}`) {
    return res.status(401).end('Unauthorized');
  }

  // Run the Python script
  exec('python3 script.py', (err, stdout, stderr) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    if (stderr) {
      return res.status(500).json({ error: stderr });
    }

    // If the script runs successfully, return the output
    res.status(200).json({ message: stdout });
  });
}
