# pdf2hashcat - Automatic PDF Password Cracker

A pure Bash tool that automatically cracks encrypted PDFs, removes the password, and opens them.

## Features

- **Fully automatic** - Just run `./pdf2hashcat encrypted.pdf` and it does everything
- **Pure Bash** - No Python, Perl, or external libraries required
- **Universal PDF support** - Works with all PDF versions:
  - PDF 1.1-1.3 (Acrobat 2-4) - RC4-40 bit encryption
  - PDF 1.4-1.6 (Acrobat 5-8) - RC4-128 bit encryption
  - PDF 1.4-1.6 (Acrobat 5-8) - AES-128 bit encryption
  - PDF 1.7 Extension Level 3 (Acrobat 9-X) - AES-256 bit encryption
  - PDF 1.7 Extension Level 8 (Acrobat XI+) - AES-256 bit encryption
- **Complete workflow** - Extracts hash, cracks password, decrypts PDF, and opens it
- **Auto-detects rockyou.txt** - No need to specify wordlist path
- **Auto-selects hashcat mode** - Detects encryption type automatically
- **Auto-decrypts PDF** - Removes password using qpdf or pdftk
- **Auto-opens result** - Opens the decrypted PDF automatically
- **Lightweight** - Uses only standard Unix/Linux tools (grep, awk, xxd)
- **Pass-through arguments** - Forward additional options to hashcat (workload, optimization, etc.)

## Requirements

- Bash 4.0 or higher
- Standard Unix tools: grep, awk, xxd, tr, head, cat
- **hashcat** - For password cracking (`apt install hashcat`)
- **qpdf** or **pdftk** - For PDF decryption (`apt install qpdf`)
- **rockyou.txt** wordlist (typically at `/usr/share/wordlists/rockyou.txt` on Kali/Debian)
- **xdg-open** or **open** - For opening PDFs (usually pre-installed)

## Installation

```bash
chmod +x pdf2hashcat
```

## Usage

### Default Mode (Automatic - Recommended)

**Simply run with the PDF file - that's it!**

```bash
# Automatically cracks, decrypts, and opens the PDF
./pdf2hashcat encrypted.pdf
```

This will:
1. Extract the password hash
2. Crack it with rockyou.txt (auto-detected)
3. Remove the password from the PDF
4. Save as `filename_decrypted.pdf`
5. Automatically open the decrypted PDF

### Additional Options

**Verbose mode (see what's happening):**
```bash
./pdf2hashcat -v encrypted.pdf
```

**Custom wordlist:**
```bash
./pdf2hashcat -w mywords.txt encrypted.pdf
```

**Hashcat optimizations:**
```bash
# Use workload profile 4 and optimized kernel
./pdf2hashcat -w 4 -O encrypted.pdf
```

**Brute force attacks:**
```bash
# 4-digit PIN
./pdf2hashcat -- -a 3 ?d?d?d?d encrypted.pdf

# 6 characters (any type)
./pdf2hashcat -- -a 3 ?a?a?a?a?a?a encrypted.pdf
```

### Extract Mode (Hash Only)

**If you just want the hash without cracking:**
```bash
# Extract hash to stdout
./pdf2hashcat -e encrypted.pdf

# Save hash to file
./pdf2hashcat -e encrypted.pdf > hash.txt
```

### Help

```bash
./pdf2hashcat -h
```

## How It Works

The script provides a complete automated workflow:

```bash
./pdf2hashcat encrypted.pdf
```

**Step 1: Extract Hash**
- Parses PDF structure to find encryption dictionary
- Extracts encryption parameters (V, R, P, O, U, OE, UE, Perms, ID)
- Formats hash for hashcat

**Step 2: Crack Password**
- Auto-detects correct hashcat mode (10400, 10500, 10600, or 25400)
- Finds rockyou.txt automatically
- Runs hashcat with optimal settings

**Step 3: Decrypt PDF**
- Extracts the cracked password
- Uses qpdf or pdftk to remove password
- Saves as `filename_decrypted.pdf`

**Step 4: Open PDF**
- Automatically opens the decrypted PDF with default viewer
- Uses xdg-open (Linux) or open (macOS)

### Manual Mode (Traditional Method)

If you prefer the traditional two-step approach:

#### PDF 1.1-1.3 (RC4-40)
```bash
./pdf2hashcat document.pdf > hash.txt
hashcat -m 10400 hash.txt wordlist.txt
```

#### PDF 1.4-1.6 (RC4-128)
```bash
./pdf2hashcat document.pdf > hash.txt
hashcat -m 10500 hash.txt wordlist.txt
```

#### PDF 1.4-1.6 (AES-128)
```bash
./pdf2hashcat document.pdf > hash.txt
hashcat -m 25400 hash.txt wordlist.txt
```

#### PDF 1.7+ (AES-256)
```bash
./pdf2hashcat document.pdf > hash.txt
hashcat -m 10600 hash.txt wordlist.txt
```

## Hashcat Mode Reference

| Mode  | Description |
|-------|-------------|
| 10400 | PDF 1.1-1.3 (Acrobat 2-4), RC4-40 |
| 10500 | PDF 1.4-1.6 (Acrobat 5-8), RC4-128 |
| 10600 | PDF 1.7 Level 3-8 (Acrobat 9+), AES-256 |
| 10700 | PDF 1.4-1.6 (Acrobat 5-8), RC4-128 (user password) |
| 25400 | PDF 1.4-1.6 (Acrobat 5-8), AES-128 |

## How It Works

The script:

1. **Parses PDF structure** - Reads the PDF file and locates the encryption dictionary
2. **Extracts encryption parameters** - Gets version (V), revision (R), permissions (P), and encryption strings (O, U, OE, UE, Perms)
3. **Retrieves document ID** - Extracts the unique document identifier from the PDF trailer
4. **Formats for hashcat** - Creates properly formatted hash string based on encryption type

## Example Output

```
$pdf$4*4*128*-1028*1*16*a1b2c3d4e5f6g7h8*32*u9i8o7p6q5w4e3r2t1y0*48*o0p9i8u7y6t5r4e3w2q1
```

## Quick Start Examples

### Complete Workflow Examples

**Example 1: Crack a PDF (simplest!)**
```bash
./pdf2hashcat secret.pdf
```
Output: Cracks password, creates `secret_decrypted.pdf`, and opens it automatically

**Example 2: Crack with GPU optimization**
```bash
./pdf2hashcat -w 4 -O secret.pdf
```

**Example 3: Brute force a 4-digit PIN protected PDF**
```bash
./pdf2hashcat -- -a 3 ?d?d?d?d invoice.pdf
```

**Example 4: Extract hash for later cracking**
```bash
./pdf2hashcat -e document.pdf > hash.txt
# Later, on a more powerful machine:
hashcat -m 10600 hash.txt huge_wordlist.txt
```

**Example 5: Use custom wordlist**
```bash
./pdf2hashcat -w /path/to/custom.txt report.pdf
```

## Troubleshooting

### "Not a valid PDF file"
- Ensure the file is actually a PDF
- Check if the file is corrupted

### "No encryption found"
- The PDF may not be password-protected
- The PDF might use a newer unsupported encryption method

### "Could not extract encryption parameters"
- The PDF structure may be malformed
- Try the `-v` flag to see what parameters were found

### "hashcat not found in PATH"
- Install hashcat: `apt install hashcat` or download from https://hashcat.net/hashcat/
- Or use extract-only mode (`-e` flag) and run hashcat manually

### "qpdf or pdftk not found"
- Install qpdf (recommended): `apt install qpdf` or `brew install qpdf`
- Or install pdftk: `apt install pdftk`
- Script will show password so you can manually decrypt

### Password not found
- Try a larger wordlist: `./pdf2hashcat -w /path/to/bigger.txt file.pdf`
- Try different attack modes (brute force, mask attack, combinator)
- For R=3/4, the script auto-tries mode 10500; manually try 25400 if needed

### PDF doesn't open automatically
- Script still saves decrypted PDF as `filename_decrypted.pdf`
- Manually open it from that location
- Install xdg-open: `apt install xdg-utils` (Linux)

## Supported Encryption Types

The script handles all standard PDF encryption specifications:

- **Standard Security Handler (Revision 2)** - 40-bit RC4
- **Standard Security Handler (Revision 3)** - 128-bit RC4
- **Standard Security Handler (Revision 4)** - 128-bit AES
- **Standard Security Handler (Revision 5)** - 256-bit AES (Extension Level 3)
- **Standard Security Handler (Revision 6)** - 256-bit AES (Extension Level 8)

## Legal Notice

This tool is intended for:
- Password recovery of your own documents
- Authorized security testing and penetration testing
- Educational purposes and security research
- CTF competitions and challenges

**Only use this tool on PDFs you own or have explicit written permission to test.**

## Technical Details

### PDF Encryption Structure

The script extracts these key components from the PDF:

- **V** - Encryption algorithm version
- **R** - Standard security handler revision
- **P** - Permission flags
- **O** - Owner password hash
- **U** - User password hash
- **OE** - Owner encryption key (R5/6 only)
- **UE** - User encryption key (R5/6 only)
- **Perms** - Encrypted permissions (R5/6 only)
- **ID** - Document identifier from trailer

### Hash Format

The output follows hashcat's expected format:

```
$pdf$V*R*keylen*P*EncryptMetadata*id_len*id*u_len*u*o_len*o[*oe_len*oe*ue_len*ue*perms_len*perms]
```

Where bracketed fields are only present for PDF 1.7+ (R5/6).

## Why Bash?

- Available by default on virtually all Unix/Linux systems
- No additional languages required (Python, Perl, Ruby, etc.)
- Uses only standard Unix tools (grep, awk, xxd, tr)
- Lightweight and fast
- Easy to read and modify
- Cross-platform compatible
- Perfect for quick security assessments

## Contributing

This tool is part of a security research project. Contributions welcome for:
- Supporting additional PDF encryption methods
- Performance improvements
- Better error handling
- Additional output formats

## License

Use responsibly and ethically. This tool should only be used for legitimate security testing purposes.
