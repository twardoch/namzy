// this_file: src/main.rs

use clap::Parser;
use namzy::{Options, generate};

#[derive(Parser, Debug)]
#[command(name = "namzy", about = "Generate fun human-friendly project names")]
struct Cli {
    /// Fetch words from online API (falls back to offline on error)
    #[arg(long, default_value_t = false)]
    online: bool,

    /// Number of names to generate
    #[arg(long, default_value_t = 1)]
    count: usize,

    /// Random seed (default: current timestamp)
    #[arg(long)]
    seed: Option<u64>,
}

fn main() {
    let cli = Cli::parse();

    for i in 0..cli.count {
        let seed = cli.seed.map(|s| s.wrapping_add(i as u64));
        let opts = Options {
            online: cli.online,
            seed,
        };
        println!("{}", generate(&opts));
    }
}
