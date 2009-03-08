package de.endrullis.utils.logging;

import java.io.PrintWriter;
import java.io.StringWriter;
import java.text.DateFormat;
import java.util.Date;
import java.util.logging.*;

/**
 * Very simple Formatter for log entries. The difference between the this one
 * and the VerySimpleFormatter is: this one prints out the class name too.
 *
 * @author Stefan Endrullis &lt;stefan@endrullis.de&gt;
 */
public class VerySimpleClassNameFormatter extends Formatter {
	private boolean printPackage = false;
	// time in format hh:mm:ss
	private DateFormat dateFormat = DateFormat.getTimeInstance(DateFormat.MEDIUM);

	public VerySimpleClassNameFormatter() {
		configure();
	}

	public String format(LogRecord record) {
		StringBuffer sb = new StringBuffer();

		sb.append(dateFormat.format(new Date(System.currentTimeMillis())));
		sb.append(" ");
		sb.append(record.getLevel().getLocalizedName());
		sb.append(": ");
		if (printPackage) {
			sb.append(record.getLoggerName());
		} else {
			sb.append(record.getLoggerName().replaceFirst("([a-z]\\w*\\.)*", ""));
		}
		sb.append(": ");
		sb.append(formatMessage(record));
		sb.append("\n");
		// exception handling
		if (record.getThrown() != null) {
			try {
				StringWriter sw = new StringWriter();
				PrintWriter pw = new PrintWriter(sw);
				record.getThrown().printStackTrace(pw);
				pw.close();
				sb.append(sw.toString());
			} catch (Exception ex) {
			}
		}

		return sb.toString();
	}

	/**
	 * Configures the logger from LogManager properties.
	 */
	private void configure() {
		String cname = getClass().getName();

		printPackage = getBooleanProperty(cname + ".printPackage", false);
	}

	/**
	 * Copy of {@link java.util.logging.LogManager@getBooleanProperty(String, boolean)}
	 */
	boolean getBooleanProperty(String name, boolean defaultValue) {
		LogManager manager = LogManager.getLogManager();
		
		String val = manager.getProperty(name);
		if (val == null) {
				return defaultValue;
		}
		val = val.toLowerCase();
		if (val.equals("true") || val.equals("1")) {
				return true;
		} else if (val.equals("false") || val.equals("0")) {
				return false;
		}
		return defaultValue;
	}
}
