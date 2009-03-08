package de.endrullis.utils.logging;

import java.io.InputStream;
import java.io.IOException;
import java.util.logging.LogManager;

/**
 * @author Stefan Endrullis &lt;stefan@endrullis.de&gt;
 */
public class LoggingUtils {
	public static void initLogManager(String resource) {
		InputStream in = LoggingUtils.class.getResourceAsStream(resource);
		LogManager lm = LogManager.getLogManager();
		try {
			lm.readConfiguration(in);
		} catch (IOException e) {
			System.err.println("WARNING: no custom logging.properties found");
		} catch (NullPointerException e) {
			System.err.println("WARNING: custom logging.properties not loaded because of NullPointerException;" +
					" this may be OK, when you are running OCS inside of tomcat");
		}
	}
}
