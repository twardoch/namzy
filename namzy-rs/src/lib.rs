// this_file: src/lib.rs

mod mangle;
mod wordlist;

pub use mangle::{apply_rotation, build_name, Mulberry32};
pub use wordlist::{BAD_SEAMS, ROTATIONS, STEMS};

use std::time::{SystemTime, UNIX_EPOCH};

pub struct Options {
    pub seed: Option<u64>,
}

fn default_seed() -> u64 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_nanos() as u64
}

pub fn generate(opts: &Options) -> String {
    let seed = opts.seed.unwrap_or_else(default_seed);
    let mut rng = Mulberry32::new(seed);
    build_name(&mut rng)
}

pub fn generate_many(count: usize, opts: &Options) -> Vec<String> {
    let base = opts.seed.unwrap_or_else(default_seed);
    (0..count)
        .map(|i| {
            let seed = base.wrapping_add((i as u64).wrapping_mul(2654435761));
            generate(&Options { seed: Some(seed) })
        })
        .collect()
}
