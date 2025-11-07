# pdf2hashcat - PDF Password Hash Extractor

A pure Bash tool to extract password hashes from encrypted PDF files for use with hashcat.

## Features

- **Pure Bash** - No Python, Perl, or external libraries required
- **Universal PDF support** - Works with all PDF versions:
  - PDF 1.1-1.3 (Acrobat 2-4) - RC4-40 bit encryption
  - PDF 1.4-1.6 (Acrobat 5-8) - RC4-128 bit encryption
  - PDF 1.4-1.6 (Acrobat 5-8) - AES-128 bit encryption
  - PDF 1.7 Extension Level 3 (Acrobat 9-X) - AES-256 bit encryption
  - PDF 1.7 Extension Level 8 (Acrobat XI+) - AES-256 bit encryption
- **Automatic hashcat integration** - Detects encryption type and runs hashcat with correct mode
- **Lightweight** - Uses only standard Unix/Linux tools (grep, sed, awk, xxd)
- **Hashcat-ready output** - Formats hashes for direct use with hashcat
- **Two modes** - Extract-only mode or automatic crack mode with `-c` flag
- **Verbose mode** - Debug output for troubleshooting
- **Pass-through arguments** - Forward additional options to hashcat (workload, optimization, etc.)

## Requirements

- Bash 4.0 or higher
- Standard Unix tools: grep, awk, xxd, tr, head, cat
- Available by default on virtually all Linux/Unix systems

## Installation

```bash
chmod +x pdf2hashcat.sh
```

## Usage

The script has two modes:
1. **Extract Mode** (default) - Just extracts and outputs the hash
2. **Crack Mode** (`-c` flag) - Extracts the hash AND automatically runs hashcat with the correct mode

### Extract Mode (Default)

```bash
# Extract hash to stdout
./pdf2hashcat.sh encrypted_document.pdf

# Save hash to file
./pdf2hashcat.sh encrypted_document.pdf > hash.txt

# Verbose mode
./pdf2hashcat.sh -v encrypted_document.pdf
```

### Crack Mode (Automatic Hashcat Integration)

```bash
# Automatically extract and crack with wordlist
./pdf2hashcat.sh -c rockyou.txt encrypted_document.pdf

# With full path to wordlist
./pdf2hashcat.sh -c /usr/share/wordlists/rockyou.txt encrypted.pdf

# With additional hashcat options (workload, optimized kernel)
./pdf2hashcat.sh -c rockyou.txt -w 3 -O encrypted.pdf

# Verbose mode + cracking
./pdf2hashcat.sh -v -c rockyou.txt encrypted.pdf

# Brute force attack (6 character all chars)
./pdf2hashcat.sh -c - -- -a 3 ?a?a?a?a?a?a encrypted.pdf

# Brute force with mask (4 digit PIN)
./pdf2hashcat.sh -c - -- -a 3 ?d?d?d?d encrypted.pdf
```

### Help

```bash
./pdf2hashcat.sh -h
```

## Using with Hashcat

### Automatic Mode (Recommended)

The script automatically detects the PDF encryption type and uses the correct hashcat mode:

```bash
# The script picks the right mode automatically!
./pdf2hashcat.sh -c rockyou.txt encrypted.pdf
```

The script will:
1. Detect PDF version and encryption type
2. Extract the hash
3. Automatically select the correct hashcat mode (10400, 10500, 10600, or 25400)
4. Run hashcat with that mode
5. Display the cracked password if successful

### Manual Mode (Traditional Method)

If you prefer the traditional two-step approach:

#### PDF 1.1-1.3 (RC4-40)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 10400 hash.txt wordlist.txt
```

#### PDF 1.4-1.6 (RC4-128)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 10500 hash.txt wordlist.txt
```

#### PDF 1.4-1.6 (AES-128)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
hashcat -m 25400 hash.txt wordlist.txt
```

#### PDF 1.7+ (AES-256)
```bash
./pdf2hashcat.sh document.pdf > hash.txt
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

**Example 1: Crack a PDF with a common wordlist**
```bash
./pdf2hashcat.sh -c /usr/share/wordlists/rockyou.txt secret.pdf
```

**Example 2: Brute force a 4-digit PIN protected PDF**
```bash
./pdf2hashcat.sh -c - -- -a 3 ?d?d?d?d invoice.pdf
```

**Example 3: Extract hash for later cracking**
```bash
./pdf2hashcat.sh document.pdf > hash.txt
# Later, on a more powerful machine:
hashcat -m 10600 hash.txt huge_wordlist.txt
```

**Example 4: Aggressive cracking with optimization**
```bash
./pdf2hashcat.sh -c rockyou.txt -w 4 -O report.pdf
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
- Or use extract-only mode (without `-c` flag) and run hashcat manually

### Password not found
- Try a larger wordlist
- Try different attack modes (brute force, mask attack, combinator)
- For R=3/4, try both modes 10500 and 25400 if one doesn't work

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
